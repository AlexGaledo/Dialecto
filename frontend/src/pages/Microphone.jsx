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
            recognition.lang = 'ceb-PH';  // Adjust language as needed
            recognition.start();

            recognition.onresult = (event) => {
                const recognizedText = event.results[0][0].transcript;
                setAudioText(recognizedText); // Update audio text state

                // Send the recognized text to your backend (or process it here)
                setResponse(`You said: ${recognizedText}`);
                setLoading(false);  // Set loading to false after receiving the result
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
                {response && <p>Response: {response}</p>}
            </div>
        </div>
    );
}
