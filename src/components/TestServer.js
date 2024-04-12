import { useState, useEffect } from "react";
import fetchServer from "../hooks/fetchServer";
import "../styles/TestServer.css";
import BeatLoader from "react-spinners/BeatLoader";


function TestServer() {
    let sleep_message = "Please wait for the server to wake up. This may take a moment or two since we're still using the free-tier Render.com for the backend."
    let [serverStatus, setServerStatus] = useState(sleep_message);

    // For the loading spinner
    let [loading, setLoading] = useState(true);
    let [color, setColor] = useState("#ff8833");
    let [speed, setSpeed] = useState(0.5);

    useEffect(() => {

        const fetchProjectData = async () => {
            await new Promise(resolve => setTimeout(resolve, 2000));
            const fetchedData = await fetchServer("server_ready");
            setServerStatus(fetchedData["message"]);
            setColor("green");
            setSpeed(0.00001);
            setLoading(true);
        };
        fetchProjectData();
    }, []);

    return (
        <>
            <div>
                <div className="testing-server">{serverStatus}</div>
                <BeatLoader
                    color={color}
                    loading={loading}
                    cssOverride={{
                        display: "block",
                        margin: "0 auto",
                    }}
                    size={10}
                    speedMultiplier={speed}
                    aria-label="Loading Spinner"
                    data-testid="loader"
                />
            </div>
        </>
    )
}

export default TestServer;