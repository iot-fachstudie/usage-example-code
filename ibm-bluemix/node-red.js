function setNewLight(light) {
    context.set("prev-light", light);
    var value = 1 - light;
    var sat = Math.min(255, value * 400);
    var brightness = Math.max(0, Math.min(255, 555-value * 600));
    var hue = 6000;
    return { payload:{
            "sat": sat,
            "bri":brightness,
            "hue": hue
    }};
}

function changeLight(light, oldLight) {
    if (oldLight === null || (oldLight === 0) && light !== 0) {
        return true;
    } else {
        return Math.abs(1 - light/oldLight) > 0.1
    }
}

if (msg.payload.light === null) {
    return null;
}
var light = msg.payload.light;
var prevLight = context.get("prev-light") || null;

if (changeLight(light, prevLight)) {
    return setNewLight(light);
} else {
    return null;
}
