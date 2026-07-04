import API from "../api";

function AssemblePanel({
  selected
}) {
  const assemble = async () => {
    const res = await API.post(
      "/assemble",
      selected
    );

    const downloadPath =
      res.data.download;

    window.open(
      `http://127.0.0.1:8000/${downloadPath}`
    );
  };

  return (
    <div className="assemble-panel">
      <p>
        Total Sections:{" "}
        {selected.length}
      </p>

      <button
  className="assemble-btn"
  onClick={assemble}
  disabled={selected.length === 0}
>
  Assemble & Download
</button>
    </div>
  );
}

export default AssemblePanel;