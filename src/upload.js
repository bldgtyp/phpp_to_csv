import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

const UploadComponent = () => {
    const [isDragOver, setIsDragOver] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDragOver = (event) => {
        setIsDragOver(true);
        event.preventDefault();
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        setSelectedFile(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log('Response from server:', response.data);
            // Handle response data as needed
        } catch (error) {
            console.error('Error uploading file:', error);
            // Handle error
        }
    };

    return (
        <div>
            <div
                onDrop={handleDrop}
                onDragEnter={handleDragOver}
                onDragOver={handleDragOver}
                onDragLeave={() => setIsDragOver(false)}
                onMouseOut={() => setIsDragOver(false)}
                className={isDragOver ? 'drag-over' : ''}
                style={
                    {
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        border: '2px dashed #ccc',
                        height: "100px",
                        margin: '40px',
                        textAlign: 'center'
                    }
                }
            >
                <p>{selectedFile ? selectedFile.name : "Drag and drop PHPP file here."}</p>
            </div>
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
};

export default UploadComponent;