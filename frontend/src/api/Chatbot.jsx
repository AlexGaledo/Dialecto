

export async function getChatbotResponse(){
    const response = await fetch("http://localhost:5000/chatbot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });
    
      const data = await response.json();
      return data;
}