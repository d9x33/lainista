import React from "react";
import "../static/css/lainista.css";
import lain from "../static/img/lain.png";
import redditData from "./data/reddit_data.json";

const Lainista = () => {
  return (
    <React.Fragment>
      {Object.entries(redditData)[0].forEach((val, key) => {
        Object.entries(val).forEach((val, key) => console.log(val));
      })}
      <div className="wallpaper">
        <h1>Lain Statistics</h1>
        <img src={lain} alt="lain" />
      </div>
      <div className="mood">
        <h2>
          Lain's mood according to <span className="yellow">TODAY's</span>{" "}
          statistics is
        </h2>
        <h2>
          {redditData["mood"]["today"] === 1 ? (
            <React.Fragment>
              <span className="positive"> POSITIVE </span>with a roughly{" "}
              <span className="positive">
                +
                {Math.round(redditData["percentage_change"]["today"] * 1000) /
                  1000}
              </span>{" "}
              percentage increase.
            </React.Fragment>
          ) : (
            <React.Fragment>
              <span className="negative"> NEGATIVE </span>with a roughly{" "}
              <span className="negative">
                -
                {Math.round(redditData["percentage_change"]["today"] * 1000) /
                  1000}
              </span>{" "}
              percentage drop.
            </React.Fragment>
          )}
        </h2>
      </div>
      <div className="bottom">
        <div className="bottom__google">
          <div className="bottom__header">Google data</div>
          <h1>sex</h1>
        </div>
        <div className="bottom__reddit">
          <div className="bottom__header">Reddit data</div>
        </div>
      </div>
    </React.Fragment>
  );
};

export default Lainista;
