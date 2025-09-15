import { createClient } from 'https://esm.sh/@supabase/supabase-js'

// Supabase anon key (safe for frontend)
const supabase = createClient(
  'https://YOUR_PROJECT.supabase.co',
  'YOUR_ANON_KEY'
)

async function fetchOHLC(ticker = "SPY") {
  let { data, error } = await supabase
	.from('ohlc_data')
	.select('*')
	.eq('ticker', ticker)
	.order('timestamp', { ascending: true })

  if (error) {
	console.error(error)
	return []
  }
  return data
}

async function drawChart() {
  const data = await fetchOHLC("SPY")

  let times = data.map(d => new Date(d.timestamp).getTime()/1000)
  let o = data.map(d => d.open)
  let h = data.map(d => d.high)
  let l = data.map(d => d.low)
  let c = data.map(d => d.close)

  let opts = {
	title: "SPY OHLC",
	width: 800,
	height: 400,
	series: [
	  { label: "Time" },
	  { label: "Open" },
	  { label: "High" },
	  { label: "Low" },
	  { label: "Close" }
	]
  }

  new uPlot(opts, [times, o, h, l, c], document.getElementById("chart"))
}

drawChart()
