import { useState } from 'react';
import axios from 'axios';
import '../styles/Upload.css';
import constants from "../data/constants.json";
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import GridLoader from "react-spinners/GridLoader";


const UploadComponent = () => {
    const API_BASE_URL = process.env.REACT_APP_API_URL || constants.RENDER_API_BASE_URL;
    const ROUTE = API_BASE_URL + 'upload';
    const [dropZoneClassName, setDropZoneClassName] = useState('file-upload-zone');
    const [selectedFile, setSelectedFile] = useState(null);
    const [isDragOver, setIsDragOver] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [processing, setProcessing] = useState(false);
    const [uploadButtonIsDisabled, setUploadButtonIsDisabled] = useState(true);

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a PHPP file to upload.');
            return;
        }

        setProcessing(true);
        setUploadButtonIsDisabled(true);

        const formData = new FormData();
        formData.append('file', selectedFile);

        axios.post(ROUTE, formData, {
            responseType: 'blob',
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: (progressEvent) => {
                const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                setUploadProgress(percentCompleted);
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

                    // Set the upload bar
                    setUploadProgress(0.0)

                    // Reset the selected file
                    setSelectedFile(null);

                    // Reset the processing state
                    setProcessing(false);

                    // Give the user a success alert message
                    alert('Success! Your PHPP has been processed. Please check your "downloads" folder for the results .ZIP file.');

                } else if (contentType === 'application/json') {
                    // Handle the JSON response
                    const reader = new FileReader();
                    reader.onload = function () {
                        const responseObject = JSON.parse(this.result);
                        alert(responseObject.error);
                    };
                    reader.readAsText(new Blob([response.data]));
                }
                setUploadButtonIsDisabled(false);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while processing the file. Please try again.')
            });
    };

    // Drag and drop event handlers
    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (e) => {
        setUploadButtonIsDisabled(false);
        setDropZoneClassName('file-upload-zone-dropped');
        setIsDragOver(false);
        e.preventDefault();
        e.stopPropagation();
        setSelectedFile(e.dataTransfer.files[0]);
    };

    return (
        <div>
            <div
                onDrop={handleDrop}
                className={`${isDragOver ? 'file-upload-zone-drag-over' : dropZoneClassName}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
            >
                <div>
                    {processing ? <div style={{ display: "flex", alignItems: "center", flexDirection: "row" }}>
                        <p>Please Wait. Processing...   </p>
                        <GridLoader
                            color="#1976d2"
                            loading={processing}
                            cssOverride={{
                                display: "block",
                                margin: "0 auto",
                            }}
                            size="5px"
                            speedMultiplier="0.85"
                            aria-label="Loading Spinner"
                            data-testid="loader"
                        />
                    </div> :
                        <p>{selectedFile ? selectedFile.name : "Drag and drop PHPP file here."}</p>
                    }
                </div>
                <div className="upload-progress-bar-empty" style={{ width: "75%" }}>
                    <div className="upload-progress-bar-fill" style={{ width: `${uploadProgress}%` }} />
                </div>
            </div>
            <Button
                onClick={handleUpload}
                component="label"
                role={undefined}
                variant="contained"
                tabIndex={-1}
                startIcon={<CloudUploadIcon />}
                disabled={uploadButtonIsDisabled}
            >
                Upload file
            </Button>
        </div>
    );
};

export default UploadComponent;