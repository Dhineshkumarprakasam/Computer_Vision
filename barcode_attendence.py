import cv2
import numpy as np
from pyzbar import pyzbar
from datetime import datetime
import pandas as pd
import os
import re


class AttendanceScanner:
    def __init__(self, camera_source, student_csv='student.csv', log_csv='attendance_log.csv'):
        self.camera_source = camera_source
        self.student_csv = student_csv
        self.log_csv = log_csv
        self.cap = None
        self.running = False
        self.last_decoded = None
        self.last_decode_time = 0
        self.decode_cooldown = 3  # 3 seconds cooldown
        self.students_df = None
        self.contrast = 1.5
        self.brightness = 10
        
        # Load student data
        self.load_students()
        
        # Create log file if doesn't exist
        self.init_log_file()
        
    def load_students(self):
        """Load student data from CSV"""
        try:
            self.students_df = pd.read_csv(self.student_csv)
            print(f"✓ Loaded {len(self.students_df)} students from {self.student_csv}")
            print(f"  Columns: {list(self.students_df.columns)}")
        except FileNotFoundError:
            print(f"✗ Error: {self.student_csv} not found!")
            print("  Please create student.csv with columns: regno, name")
            exit(1)
        except Exception as e:
            print(f"✗ Error loading student data: {e}")
            exit(1)
    
    def init_log_file(self):
        """Initialize attendance log CSV"""
        if not os.path.exists(self.log_csv):
            # Create with headers
            df = pd.DataFrame(columns=['regno', 'name', 'date', 'day', 'month', 'year', 'time', 'period'])
            df.to_csv(self.log_csv, index=False)
            print(f"✓ Created {self.log_csv}")
        else:
            print(f"✓ Using existing {self.log_csv}")
    
    def extract_regno(self, text):
        """Extract registration number pattern like 23BCS0022"""
        # Pattern: 2 digits + 3 letters + 4 digits
        pattern = r'\b\d{2}[A-Z]{3}\d{4}\b'
        match = re.search(pattern, text.upper())
        return match.group(0) if match else None
    
    def validate_student(self, regno):
        """Check if regno exists in student database"""
        if self.students_df is None:
            return None
        
        student = self.students_df[self.students_df['regno'] == regno]
        if not student.empty:
            return student.iloc[0]['name']
        return None
    
    def log_attendance(self, regno, name):
        """Log attendance to CSV with timestamp breakdown"""
        now = datetime.now()
        
        # Extract time components
        date = now.strftime('%d')
        day = now.strftime('%A')
        month = now.strftime('%B')
        year = now.strftime('%Y')
        time_str = now.strftime('%I:%M:%S')
        period = now.strftime('%p')
        
        # Create record
        record = {
            'regno': regno,
            'name': name,
            'date': date,
            'day': day,
            'month': month,
            'year': year,
            'time': time_str,
            'period': period
        }
        
        # Append to CSV
        df = pd.DataFrame([record])
        df.to_csv(self.log_csv, mode='a', header=False, index=False)
        
        return record
    
    def print_csv_header(self):
        """Print CSV header"""
        print("REG NO, NAME, STATUS, TIMESTAMP")
        print("-" * 80)
    
    def print_csv_row(self, regno, name, status, record=None):
        """Print comma-separated row with combined timestamp"""
        if status == "✓ PRESENT" and record:
            # Format: DD-Day-Month-YYYY HH:MM:SS PM/AM
            timestamp = f"{record['date']}-{record['day']}-{record['month']}-{record['year']} {record['time']} {record['period']}"
            print(f"{regno}, {name}, {status}, {timestamp}")
        elif status == "INVALID (Not in DB)":
            print(f"{regno}, {name}, {status}, ---")
        else:  # Invalid format
            print(f"{regno}, {name}, {status}, ---")
    
    def initialize_camera(self):
        """Initialize camera"""
        self.cap = cv2.VideoCapture(self.camera_source)
        if not self.cap.isOpened():
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        return True
    
    def fast_decode(self, frame):
        """Fast barcode decoding"""
        # Try grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.convertScaleAbs(gray, alpha=self.contrast, beta=self.brightness)
        
        # Quick decode
        barcodes = pyzbar.decode(enhanced)
        if barcodes:
            return barcodes
        
        # Try threshold
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        barcodes = pyzbar.decode(thresh)
        
        return barcodes
    
    def draw_detection(self, frame, barcode, is_valid, name=""):
        """Draw detection box on frame"""
        points = barcode.polygon
        
        # Color based on validity
        color = (0, 255, 0) if is_valid else (0, 0, 255)
        
        if len(points) == 4:
            pts = np.array([(p.x, p.y) for p in points], dtype=np.int32)
            cv2.polylines(frame, [pts.reshape((-1, 1, 2))], True, color, 3)
        
        x = barcode.rect.left
        y = barcode.rect.top
        w = barcode.rect.width
        h = barcode.rect.height
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        
        # Display text
        data = barcode.data.decode('utf-8')
        
        if is_valid:
            text1 = f"VALID: {data}"
            text2 = f"Name: {name}"
            cv2.rectangle(frame, (x, y - 60), (x + max(len(text1), len(text2)) * 10, y), (0, 255, 0), -1)
            cv2.putText(frame, text1, (x + 5, y - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(frame, text2, (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        else:
            text = f"INVALID: {data}"
            cv2.rectangle(frame, (x, y - 35), (x + len(text) * 10, y), (0, 0, 255), -1)
            cv2.putText(frame, text, (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def start(self):
        """Start attendance scanning"""
        if not self.initialize_camera():
            print("✗ Camera failed")
            return
        
        self.running = True
        
        print("\n" + "="*80)
        print(" " * 25 + "STUDENT ATTENDANCE SYSTEM")
        print("="*80)
        print(f"Student Database: {self.student_csv} ({len(self.students_df)} students)")
        print(f"Attendance Log: {self.log_csv}")
        print(f"Camera: {self.camera_source}")
        print("="*80)
        print("\nScanning for ID cards... Point barcode at camera")
        print("Press 'q' to quit\n")
        
        # Print CSV header
        self.print_csv_header()
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Decode barcodes
                barcodes = self.fast_decode(frame)
                
                current_time = datetime.now().timestamp()
                
                for barcode in barcodes:
                    raw_data = barcode.data.decode('utf-8')
                    
                    # Extract regno
                    regno = self.extract_regno(raw_data)
                    
                    if regno:
                        # Check if valid student
                        name = self.validate_student(regno)
                        
                        if name:
                            # Valid student
                            if regno != self.last_decoded or current_time - self.last_decode_time > self.decode_cooldown:
                                # Log attendance
                                record = self.log_attendance(regno, name)
                                
                                # Print CSV row
                                self.print_csv_row(regno, name, "✓ PRESENT", record)
                                
                                self.last_decoded = regno
                                self.last_decode_time = current_time
                            
                            # Draw on frame
                            self.draw_detection(frame, barcode, True, name)
                        else:
                            # Regno pattern found but not in database
                            if regno != self.last_decoded or current_time - self.last_decode_time > self.decode_cooldown:
                                self.print_csv_row(regno, "Not in Database", "INVALID (Not in DB)")
                                
                                self.last_decoded = regno
                                self.last_decode_time = current_time
                            
                            self.draw_detection(frame, barcode, False)
                    else:
                        # Invalid pattern
                        if raw_data != self.last_decoded or current_time - self.last_decode_time > self.decode_cooldown:
                            display_data = raw_data[:12] if len(raw_data) > 12 else raw_data
                            self.print_csv_row(display_data, "Invalid Format", "INVALID (Bad Format)")
                            
                            self.last_decoded = raw_data
                            self.last_decode_time = current_time
                        
                        self.draw_detection(frame, barcode, False)
                
                # Display info on frame
                cv2.putText(frame, "ATTENDANCE SCANNER - Scan ID Card Barcode", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cv2.putText(frame, f"Students: {len(self.students_df)} | Press 'q' to quit", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow('Attendance Scanner', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('+'):
                    self.brightness += 5
                elif key == ord('-'):
                    self.brightness -= 5
                elif key == ord(']'):
                    self.contrast += 0.1
                elif key == ord('['):
                    self.contrast = max(0.5, self.contrast - 0.1)
        
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
            print("\n" + "="*80)
            print("✓ Scanner stopped")
            print(f"✓ Attendance log saved to: {self.log_csv}")
            print("="*80)


if __name__ == "__main__":
   
    DROIDCAM_IP = 'http://10.218.99.199:4747/video'
    
    # File paths
    STUDENT_CSV = r"C:\Users\Dhineshkumar\Downloads\students.csv"   # Input: Student database
    LOG_CSV = 'attendance_log.csv'   # Output: Attendance
    
    print("Starting Attendance Scanner...")
    print(f"Camera: {DROIDCAM_IP}")
    print(f"Student DB: {STUDENT_CSV}")
    print(f"Log File: {LOG_CSV}\n")
    
    try:
        scanner = AttendanceScanner(
            camera_source=DROIDCAM_IP,
            student_csv=STUDENT_CSV,
            log_csv=LOG_CSV
        )
        scanner.start()
    except KeyboardInterrupt:
        print("\n✓ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
