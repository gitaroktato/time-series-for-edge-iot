import "influxdata/influxdb/schema"
import "math"

from(bucket: "sensors")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "controller")
  |> filter(fn: (r) => r["_field"] == "x" or r["_field"] == "y")
  |> yield(name: "points")

from(bucket: "sensors")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "controller")
  |> filter(fn: (r) => r["_field"] == "x" or r["_field"] == "y")
  |> derivative(unit: 1s, nonNegative: true)
  |> schema.fieldsAsCols()
  |> map(fn: (r) => ({ r with _value: math.mMax(x:r.x, y:r.y) }))  
  |> yield(name: "derivative")