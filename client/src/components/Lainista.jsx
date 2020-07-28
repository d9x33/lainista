import React from "react";
import "../static/css/lainista.css";
import lain from "../static/img/lain.png";
import redditData from "./data/reddit_data.json";
import googleData from "./data/google_data.json";

const Lainista = () => {
  const capitalize = (str, lower = false) =>
    (lower ? str.toLowerCase() : str).replace(/(?:^|\s|["'([{])+\S/g, (match) =>
      match.toUpperCase()
    );

  const matchAfterLastLine = (str) => {
    return str.match(/([^/]+$)/)[0].toString();
  };

  const matchUntilFirstDot = (str) => {
    return str.match(/^([^.]+)/)[0].toString();
  };

  const formatImgName = (imgName) => {
    return capitalize(
      matchUntilFirstDot(matchAfterLastLine(imgName)).replace(/_/g, " ")
    );
  };

  const displayJsonData = (data) => {
    return (
      <React.Fragment>
        {Object.entries(data["mood"]).map((element) => {
          return (
            <React.Fragment>
              <h2>
                <span className="yellow">{element[0].toUpperCase()}:</span>{" "}
                <br />
                {element[1] === 1 ? (
                  <React.Fragment>
                    <span className="positive"> POSITIVE </span>with a roughly{" "}
                    <span className="positive">
                      +
                      {Math.round(
                        data["percentage_change"][element[0]] * 1000
                      ) / 1000}
                    </span>{" "}
                    percentage increase.
                  </React.Fragment>
                ) : (
                  <React.Fragment>
                    <span className="negative"> NEGATIVE </span>with a roughly{" "}
                    <span className="negative">
                      {Math.round(
                        data["percentage_change"][element[0]] * 1000
                      ) / 1000}
                    </span>{" "}
                    percentage drop.
                  </React.Fragment>
                )}
              </h2>
            </React.Fragment>
          );
        })}
      </React.Fragment>
    );
  };

  const importAll = (r) => {
    return r.keys().map(r);
  };

  return (
    <React.Fragment>
      <div className="wallpaper">
        <h1>Lain Statistics</h1>
        <img src={lain} alt="lain" />
      </div>
      <h2 id="popularityheader">Popularity statistics</h2>
      <div className="mood">
        <div className="mood__google">
          <h2>Google</h2>
          {displayJsonData(googleData)}
        </div>
        <div className="mood__reddit">
          <h2>Reddit</h2>
          {displayJsonData(redditData)}
        </div>
      </div>
      <div className="bottom">
        <div className="bottom__google">
          <div className="bottom__header">Google charts</div>
          {importAll(
            require.context(
              "../static/plots/google",
              false,
              /\.(png|jpe?g|svg)$/
            )
          ).map((img) => {
            return (
              <React.Fragment>
                <h2 className="bottom--plotheader">{formatImgName(img)}</h2>
                <img alt="img" src={img} />
              </React.Fragment>
            );
          })}
        </div>
        <div className="bottom__reddit">
          <div className="bottom__header">Reddit charts</div>
          {importAll(
            require.context(
              "../static/plots/reddit",
              false,
              /\.(png|jpe?g|svg)$/
            )
          ).map((img) => {
            return (
              <React.Fragment>
                <h2 className="bottom--plotheader">{formatImgName(img)}</h2>
                <img alt="img" src={img} />
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </React.Fragment>
  );
};

export default Lainista;
