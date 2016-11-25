SELECT
  CASE
    WHEN brightness * 400 < 255 THEN brightness * 400
    ELSE 255
  END as 'saturation',
  CASE WHEN 555 - brightness * 600 > 0
    THEN
      CASE WHEN 555 - brightness * 600 < 255
        THEN 555 - brightness * 600
        ELSE 255
      END
    ELSE 0
  END as 'brighness',
  6000 as 'hue'
INTO
  [hue-signals]
FROM
  [brightness-sensor-data]
