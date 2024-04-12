import { useState } from 'react';
import axios from 'axios';
import '../styles/Upload.css';
import constants from "../data/constants.json";
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const UploadComponent = () => {
    const API_BASE_URL = process.env.REACT_APP_API_URL || constants.RENDER_API_BASE_URL;
    const ROUTE = API_BASE_URL + 'upload';
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
            alert('Please select a PHPP file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        axios.post(ROUTE, formData, {
            responseType: 'blob',
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .then((response) => {
                const contentType = response.headers['content-type'];
                if (contentType === 'application/zip') {
                    // Create a new Blob object from response data
                    const blob = new Blob([response.data], { type: 'application/zip' });

                    // Create a link element
                    const link = document.createElement('a');

                    // Create an object URL for the Blob
                    link.href = URL.createObjectURL(blob);

                    // Set the download attribute of the link to the desired file name
                    link.download = 'results.zip';

                    // Append the link to the document body
                    document.body.appendChild(link);

                    // Programmatically click the link to start the download
                    link.click();

                    // Remove the link from the document body
                    document.body.removeChild(link);
                } else if (contentType === 'application/json') {
                    // Handle the JSON response
                    const reader = new FileReader();
                    reader.onload = function () {
                        const responseObject = JSON.parse(this.result);
                        alert(responseObject.error);
                    };
                    reader.readAsText(new Blob([response.data]));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while processing the file. Please try again.')
            });
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
            <Button
                onClick={handleUpload}
                component="label"
                role={undefined}
                variant="contained"
                tabIndex={-1}
                startIcon={<CloudUploadIcon />}
            >
                Upload file
            </Button>
        </div>
    );
};

export default UploadComponent;