import React, { useState } from "react";
import axios from "axios";
import Services from "../Environment";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";

const Title = () => {
  const [typing, setTyping] = useState(false);
  const [messages, setMessages] = useState([
    {
      message: "Hey! , Iam PSR Engineering Chat-bot ? How Can I Help You ? ",
      sender: "PSR Chatbot",
      direction: "incoming",
    },
  ]);

  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: "User",
      direction: "outgoing",
    };

    const newMessages = [...messages, newMessage];
    setMessages(newMessages);
    setTyping(true);
    const ans = await axios
      .post(`${Services.SERVER_URL}/message`, {
        message: message,
      })
      .then((res) => {
        console.log(res.data);
        const modeMessage = {
          message: res.data.answer,
          sender: "PSR Chatbot",
          direction: "incoming",
        };

        const received = [...newMessages, modeMessage];
        setTyping(false);
        setMessages(received);
      });
  };

  return (
    <div>
      <MainContainer
        responsive
        style={{
          height: "90vh",
        }}
      >
        <ChatContainer>
          <MessageList
            typingIndicator={
              typing ? <TypingIndicator content="Please Wait " /> : null
            }
          >
            {messages.map((msg, i) => {
              return <Message key={i} model={msg} />;
            })}
          </MessageList>
          <MessageInput placeholder="Ask question... " onSend={handleSend} />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default Title;
