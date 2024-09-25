import "math"
option v = {
  timeRangeStart: -1h,
  timeRangeStop: now()
}

option task = { 
  name: "aggregate_max_accel",
  every: 5m,
}

from(bucket: "sensors")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "accel")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> map(fn: (r) => ({r with _value: math.cbrt(x: r.x) + math.cbrt(x: r.y) + math.cbrt(x: r.z)}))
  |> map(fn: (r) => ({r with _value: math.sqrt(x: r._value)}))
  |> map(fn: (r) => ({r with _field: "max_accel"}))
  |> aggregateWindow(every: 1m, fn: max, createEmpty: false)
  |> yield(name: "max")
  |> to(bucket: "max_accel")
  |> to(bucket: "max_accel", org: "docs")
  