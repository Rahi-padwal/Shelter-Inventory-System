#!/usr/bin/env python3
"""
Test file upload functionality
"""

import os
import tempfile
from app import create_app
from app.utils import allowed_file, save_uploaded_file

def test_file_upload():
    """Test file upload functionality"""
    
    print("🧪 Testing File Upload Functionality")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        # Test allowed_file function
        print("Testing file type validation...")
        
        # Valid files
        valid_files = ['image.jpg', 'photo.png', 'picture.jpeg', 'image.gif', 'photo.webp']
        for filename in valid_files:
            assert allowed_file(filename), f"Should allow {filename}"
            print(f"✅ {filename} - Valid")
        
        # Invalid files
        invalid_files = ['document.pdf', 'text.txt', 'video.mp4', 'script.js']
        for filename in invalid_files:
            assert not allowed_file(filename), f"Should not allow {filename}"
            print(f"✅ {filename} - Invalid (correctly rejected)")
        
        # Test file saving
        print("\nTesting file saving...")
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(b'fake image data')
            tmp_file_path = tmp_file.name
        
        try:
            # Create a mock file object
            class MockFile:
                def __init__(self, file_path):
                    self.filename = 'test_image.jpg'
                    self.file_path = file_path
                
                def save(self, path):
                    import shutil
                    shutil.copy2(self.file_path, path)
            
            mock_file = MockFile(tmp_file_path)
            
            # Test saving
            result = save_uploaded_file(mock_file)
            
            if result:
                print(f"✅ File saved successfully: {result}")
                
                # Check if file exists
                file_path = result.replace('/static/', 'static/')
                if os.path.exists(file_path):
                    print("✅ File exists on disk")
                    # Clean up
                    os.remove(file_path)
                    print("✅ Test file cleaned up")
                else:
                    print("❌ File not found on disk")
            else:
                print("❌ File save failed")
                
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
    
    print("\n🎉 File upload tests completed!")

if __name__ == '__main__':
    test_file_upload()
