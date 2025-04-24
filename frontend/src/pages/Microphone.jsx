import React, { useState } from 'react';

export default function Microphone() {
    const [audioText, setAudioText] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);  // To track loading state

    const handleAudioInput = async () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        // Check if the SpeechRecognition API is available in the browser        
        if (!SpeechRecognition) {
            setResponse("Speech recognition is not supported in your browser.");
            return; // Exit early if the API is unavailable
        }
    
        setLoading(true); // Set loading to true when recording starts
        try {
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';  // Adjust language as needed
            recognition.start();
    
            recognition.onresult = async (event) => {
                const recognizedText = event.results[0][0].transcript;
                setAudioText(recognizedText); // Update audio text state
    
                // Send the recognized text to your backend (or process it here)
                setResponse(`You said: ${recognizedText}`);
                
                try {
                    const res = await fetch("http://localhost:5000/chatbot", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ text: recognizedText })
                    });
    
                    if (!res.ok) {
                        console.error("Error:", res.statusText);
                        setResponse('Error fetching chatbot response');
                        setLoading(false);
                        return;
                    }
    
                    const data = await res.json();
                    setResponse(data.chatbot_response); // Correct field name here
                } catch (error) {
                    console.error('Error fetching chatbot response:', error);
                    setResponse('Error fetching chatbot response');
                }
    
                setLoading(false);  // Set loading to false after receiving the response
            };
    
            recognition.onerror = (event) => {
                console.error('Error recognizing speech:', event.error);
                setResponse('Error recognizing speech');
                setLoading(false);  // Set loading to false if there's an error
            };
        } catch (error) {
            console.error('Error with speech recognition:', error);
            setResponse('Speech recognition is not supported');
            setLoading(false);  // Set loading to false in case of an error
        }
    };
    

    return (
        <div className="microphone_container">
            <button className="microphone_button" onClick={handleAudioInput}>
                <img src="microphone.jpg" alt="Microphone" className="microphone-icon" />
                <h1>Microphone</h1>
                <p>Click to start recording</p>
            </button>

            {/* Show loading spinner when the request is being processed */}
            {loading && <div className='loading-spinner'>Loading...</div>}

            <div className="chatbot_response">
                {audioText && <p>Audio Text: {audioText}</p>}
                {response && <p>{response}</p>}
            </div>
        </div>
    );
}
