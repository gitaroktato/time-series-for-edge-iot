from(bucket: "home")
  |> range(start: -5s, stop: now())
  |> map(fn: (r) => ({ r with _value: (int(v: now()) - int(v: r._time)) / 1000000 }))
  |> last()