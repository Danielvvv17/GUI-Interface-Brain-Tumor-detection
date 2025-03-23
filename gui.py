import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFileDialog, QProgressBar, 
                           QComboBox, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from model_predictor import predict_tumor
from image_processing import auto_resize
from feedback import FeedbackManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.feedback_manager = FeedbackManager()
        self.image_path = None
        self.processing = False
        self.marker_active = False
        self.marker_points = []

    def initUI(self):
        self.setWindowTitle('Brain Tumor Detection System')
        self.setMinimumSize(1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QLabel {
                font-size: 14px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header with scientific background
        header = QLabel()
        header.setStyleSheet("""
            QLabel {
                background-color: #1565C0;
                color: white;
                padding: 20px;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        header.setText("Brain Tumor Detection System")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Image container
        self.image_container = QLabel()
        self.image_container.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #BDBDBD;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.image_container.setMinimumSize(600, 400)
        self.image_container.setAlignment(Qt.AlignCenter)
        self.image_container.setText("No image loaded")
        layout.addWidget(self.image_container)

        # Buttons container
        buttons_layout = QHBoxLayout()
        
        # Load Image button
        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)
        buttons_layout.addWidget(self.load_btn)

        # Process button
        self.process_btn = QPushButton("Process")
        self.process_btn.clicked.connect(self.process_image)
        self.process_btn.setEnabled(False)
        buttons_layout.addWidget(self.process_btn)

        # Marker button
        self.marker_btn = QPushButton("Marker")
        self.marker_btn.clicked.connect(self.toggle_marker)
        self.marker_btn.setEnabled(False)
        buttons_layout.addWidget(self.marker_btn)

        # Delete button
        self.delete_btn = QPushButton("Delete Image")
        self.delete_btn.clicked.connect(self.delete_image)
        self.delete_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_btn)

        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_processing)
        self.cancel_btn.setEnabled(False)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Result and feedback section
        result_layout = QHBoxLayout()
        
        self.result_label = QLabel("Result: ")
        result_layout.addWidget(self.result_label)
        
        self.feedback_combo = QComboBox()
        self.feedback_combo.addItems(["No Tumor", "Tumor"])
        self.feedback_combo.setEnabled(False)
        result_layout.addWidget(self.feedback_combo)
        
        self.submit_feedback_btn = QPushButton("Submit Feedback")
        self.submit_feedback_btn.clicked.connect(self.submit_feedback)
        self.submit_feedback_btn.setEnabled(False)
        result_layout.addWidget(self.submit_feedback_btn)
        
        layout.addLayout(result_layout)

        # Processing time label
        self.time_label = QLabel("Processing time: 0s")
        layout.addWidget(self.time_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", 
                                                 "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.image_container.size(), 
                                        Qt.KeepAspectRatio, 
                                        Qt.SmoothTransformation)
            self.image_container.setPixmap(scaled_pixmap)
            self.process_btn.setEnabled(True)
            self.marker_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)

    def process_image(self):
        if not self.image_path:
            return
            
        self.processing = True
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_value = 0
        self.timer.start(50)  # Update every 50ms
        
        self.load_btn.setEnabled(False)
        self.process_btn.setEnabled(False)
        self.marker_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        
        QTimer.singleShot(5000, self.complete_processing)

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value * 2)
        self.time_label.setText(f"Processing time: {self.progress_value * 0.05:.1f}s")

    def complete_processing(self):
        if not self.processing:
            return
            
        self.processing = False
        self.timer.stop()
        self.progress_bar.setVisible(False)
        self.cancel_btn.setEnabled(False)
        
        result = predict_tumor(self.image_path)
        self.result_label.setText(f"Result: {result}")
        
        self.load_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
        self.marker_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.feedback_combo.setEnabled(True)
        self.submit_feedback_btn.setEnabled(True)

    def cancel_processing(self):
        self.processing = False
        self.timer.stop()
        self.progress_bar.setVisible(False)
        self.cancel_btn.setEnabled(False)
        self.time_label.setText("Processing time: 0s")
        
        self.load_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
        self.marker_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)

    def delete_image(self):
        self.image_container.clear()
        self.image_container.setText("No image loaded")
        self.image_path = None
        self.process_btn.setEnabled(False)
        self.marker_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.feedback_combo.setEnabled(False)
        self.submit_feedback_btn.setEnabled(False)
        self.result_label.setText("Result: ")
        self.time_label.setText("Processing time: 0s")

    def toggle_marker(self):
        self.marker_active = not self.marker_active
        if self.marker_active:
            self.marker_btn.setStyleSheet("background-color: #f44336;")
            self.image_container.mousePressEvent = self.marker_press_event
        else:
            self.marker_btn.setStyleSheet("")
            self.image_container.mousePressEvent = None
            self.marker_points = []

    def marker_press_event(self, event):
        if not self.marker_active:
            return
            
        pos = event.pos()
        self.marker_points.append(pos)
        
        # Draw marker point
        pixmap = self.image_container.pixmap().copy()
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("#f44336"), 4))
        painter.drawPoint(pos)
        painter.end()
        
        self.image_container.setPixmap(pixmap)

    def submit_feedback(self):
        current_result = self.result_label.text().replace("Result: ", "")
        feedback = self.feedback_combo.currentText()
        
        if current_result != feedback:
            self.feedback_manager.update_feedback(current_result, feedback)
            QMessageBox.information(self, "Feedback", 
                                  "Thank you for your feedback! The system will learn from this.")