data = from(bucket: "sensors")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> map(fn: (r) => ({ r with _value: 1 }))
  |> group() 
  //|> yield(name: "raw-data")

datapointsPerSec = data  
  |> aggregateWindow(every: 1s, fn: sum)
  |> yield(name: "rate")

datapointsPerSec 
  |> aggregateWindow(every: v.windowPeriod, fn: mean)
  |> yield(name: "meanRate")
