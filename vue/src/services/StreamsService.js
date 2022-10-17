export const getStreams = (callback) => {
  // fetch stream details from API
  // need domain without port
  const domainParts = window.location.origin.split(":");
  const domain = `${domainParts[0]}:${domainParts[1]}`;
  const port = 5000;
  const url = `${domain}:${port}/streams`;
  fetch(url).then((jsonData) => {
    jsonData.json().then((data) => {
      callback(data.streams);
    });
  });
};

// return [
//   {
//     _id: 1,
//     title: "Example Stream",
//     url: "https://test-streams.mux.dev/x36xhzz/url_6/193039199_mp4_h264_aac_hq_7.m3u8",
//   },
//   {
//     _id: 2,
//     title: "Another Example Stream",
//     url: "https://test-streams.mux.dev/test_001/stream.m3u8",
//   },
// ];
