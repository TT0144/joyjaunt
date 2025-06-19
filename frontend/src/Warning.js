import React from "react";
import { MapPin, ArrowLeft } from "lucide-react";

const warn = () => {
  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        backgroundColor: "black",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "30rem",
          height: "935px",
          backgroundColor: "#D11C2C",
          padding: "2rem",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          color: "black",
          position: "relative",
        }}
      >
        <MapPin
          style={{ width: "6rem", height: "6rem", marginBottom: "2rem" }}
        />
        <h1
          style={{ fontSize: "3rem", fontWeight: "bold", marginBottom: "3rem" }}
        >
          危険
        </h1>
        <div
          style={{
            background:
              "linear-gradient(to bottom right, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05))",
            padding: "2rem",
            borderRadius: "1.5rem",
            boxShadow: "0 2px 8px rgba(255, 255, 255, 0.1)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            transform: "translateY(0)",
            transition: "transform 0.3s ease",
          }}
        >
          <p
            style={{
              fontSize: "1.5rem",
              fontWeight: "bold",
              textAlign: "center",
              marginBottom: "1.5rem",
              textShadow: "0 1px 2px rgba(0, 0, 0, 0.5)",
            }}
          >
            ⚠️ 現在危険地帯に立ち入りました
          </p>
          <p
            style={{
              fontSize: "1.3rem",
              textAlign: "center",
              color: "black",
              lineHeight: "1.75",
              fontWeight: "medium",
              letterSpacing: "0.05em",
            }}
          >
            直ちに離れてください
          </p>
        </div>
        <button
          onClick={() => window.history.back()}
          style={{
            position: "absolute",
            bottom: "2rem",
            left: "50%",
            transform: "translateX(-50%)",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            padding: "0.75rem 1.5rem",
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderRadius: "9999px",
            backdropFilter: "blur(8px)",
            border: "1px solid rgba(255, 255, 255, 0.2)",
            color: "white",
            fontWeight: "medium",
            transition: "background-color 0.3s ease",
          }}
        >
          <ArrowLeft style={{ width: "1.25rem", height: "1.25rem" }} />
          <span>戻る</span>
        </button>
      </div>
    </div>
  );
};

export default warn;
