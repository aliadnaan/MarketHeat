async function loadSPYData() {
	// Load SPY JSON (static for now, later can be API)
	const res = await fetch("/data/spy.json");
	const data = await res.json();

	// Build arrays
	const x = data.timestamp.map(t => t * 1000); // convert to JS time
	const o = data.open;
	const h = data.high;
	const l = data.low;
	const c = data.close;

	// Chart options
	const opts = {
		title: "SPY (Candlestick)",
		width: 800,
		height: 400,
		scales: {
			x: { time: true },
			y: {
				// Custom auto-range that uses ALL OHLC values
				range: (u, dataMin, dataMax) => {
					const oVals = u.data[1];
					const hVals = u.data[2];
					const lVals = u.data[3];
					const cVals = u.data[4];

					const min = Math.min(...oVals, ...hVals, ...lVals, ...cVals);
					const max = Math.max(...oVals, ...hVals, ...lVals, ...cVals);

					const padding = (max - min) * 0.05; // add 5% padding
					return [min - padding, max + padding];
				}
			}
		},
		series: [
			{}, // x-axis (time)
			{ label: "Open", show: false, scale: "y" },
			{ label: "High", show: false, scale: "y" },
			{ label: "Low",  show: false, scale: "y" },
			{
				label: "Close",
				scale: "y",
				paths: (u, sidx, i0, i1) => {
					const ctx = u.ctx;
					const x = u.data[0];
					const o = u.data[1];
					const h = u.data[2];
					const l = u.data[3];
					const c = u.data[4];

					for (let i = i0; i <= i1; i++) {
						if (x[i] == null) continue;

						const xPos = u.valToPos(x[i], "x", true);
						const openPos = u.valToPos(o[i], "y", true);
						const highPos = u.valToPos(h[i], "y", true);
						const lowPos = u.valToPos(l[i], "y", true);
						const closePos = u.valToPos(c[i], "y", true);

						const isUp = c[i] >= o[i];
						ctx.strokeStyle = isUp ? "green" : "red";

						// Wick
						ctx.beginPath();
						ctx.moveTo(xPos, highPos);
						ctx.lineTo(xPos, lowPos);
						ctx.stroke();

						// Body
						ctx.beginPath();
						ctx.lineWidth = 8;
						ctx.moveTo(xPos, openPos);
						ctx.lineTo(xPos, closePos);
						ctx.stroke();
						ctx.lineWidth = 1;
					}
				}
			}
		]
	};

	// Initialize chart
	new uPlot(opts, [x, o, h, l, c], document.getElementById("chart"));
}

loadSPYData();
