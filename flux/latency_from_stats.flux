latency = from(bucket: "latency")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "gyro") 
 
latency
|> yield(name: "current")
 
latency
  |> aggregateWindow(every: 1m, fn: mean)
  |> yield(name: "mean")
 
latency
  |> aggregateWindow(every: 1m, fn: (t=<-, column) => t |> quantile(q: 0.95))
  |> yield(name: "p95")
 
latency
  |> aggregateWindow(every: 1m, fn: min)
  |> yield(name: "min")