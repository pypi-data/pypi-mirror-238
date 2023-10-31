let captchaPassed = false;
const regions = ["u", "e", "j", "k"];

function isValidMAC(mac) {
	return mac.match(/^[0-9a-f]{12}$/igm) !== null;
}

function check() {
	if (!isValidMAC(document.getElementById("mac").value)) {
		return false;
	}
	let hasRegion = false;
	regions.forEach(function(item, ignore) {
		if (document.getElementById("region_" + item).checked === true) {
			hasRegion = true;
		}
	});
	if (!hasRegion) {
		return false;
	}
	if (document.getElementById("recaptcha") === null) {
		return true;
	}
	return captchaPassed;
}

function update(ok) {
	document.getElementById("submit_btn").disabled = !ok;
	document.getElementById("submit_btn2").disabled = !ok;
	document.getElementById("submit_btn3").disabled = !ok;
	document.getElementById("submit_btn4").disabled = !ok;
}

function handleInput(event) {
	const keycode = (window.event ? event.keyCode : event.which);
	// (numpad 0-9 or 0-9 or A-F)
	if ((keycode >= 97 && keycode <= 105) || (keycode >= 48 && keycode <= 57) || (keycode >= 65 && keycode <= 70)) {
		return true;
	} else {
		event.preventDefault();
		return false;
	}
}

function forceCorrectMac(ignore) {
	const mac = document.getElementById("mac");
	mac.value = mac.value.replace(/[^a-f0-9]/gi, "");
}

function captchaOK() {
	captchaPassed = true;
	update(check());
}

function captchaExpired() {
	captchaPassed = false;
	update(check());
}

function prefillUsingParams() {
	const params = new URLSearchParams(window.location.search);
	const region_param = params.get("region");
	const mac_param = params.get("mac");
	const hackmii_param = params.get("hackmii");
	if (region_param !== null && regions.includes(region_param.toLowerCase())) {
		document.getElementById("region_" + region_param.toLowerCase()).checked = true;
	}
	if (mac_param !== null && isValidMAC(mac_param.slice(0, 12))) {
		document.getElementById("mac").value = mac_param.slice(0, 12).toUpperCase();
	}
	if (hackmii_param !== null) {
		document.getElementById("hackmii").checked = ["on", "yes", "true", "checked"].includes(hackmii_param.toLowerCase());
	}
}

function putSubmittedURLParams() {
	const params = new URLSearchParams();
	const data = Object.fromEntries(new FormData(document.getElementById("bombform")));
	if (data.region !== undefined) {
		params.set("region", data.region);
	}
	if (data.mac !== undefined) {
		params.set("mac", data.mac);
	}
	if (data.hackmii !== undefined) {
		params.set("hackmii", data.hackmii);
	} else {
		params.set("hackmii", "off");
	}
	history.replaceState({}, '', `?${params.toString()}`);
}

document.addEventListener("DOMContentLoaded", function() {
	prefillUsingParams();
	update(check());
	document.getElementById("mac").addEventListener("keypress", handleInput);
	document.getElementById("mac").addEventListener("keyup", () => { update(check());});
	document.getElementById("mac").addEventListener("change", forceCorrectMac);
	regions.forEach(function(item, ignore) {
		document.getElementById("region_" + item).addEventListener(
			"change",
			() => {
				update(check());
			}
		);
	});

	document.getElementById("bombform").addEventListener("submit", function (event) {
		event.preventDefault();
		putSubmittedURLParams();
		const errorElement = document.getElementById("error");
		const hasHidden = errorElement.classList.contains("hidden");
		fetch("/", {
			method: "POST",
			body: new FormData(event.target)
		}).then(response => {
			if (response.ok) {
				return response.blob();
			} else {
				if (hasHidden) {
					errorElement.classList.remove("hidden");
				}
				response.json().then(json => {
					errorElement.innerHTML = json.message;
					throw new Error(json.message);
				});
				return null;
			}
		}).then(data => {
			if (data === null) {
				return;
			}
			if (!hasHidden) {
				errorElement.classList.add("hidden");
			}
			const blob = URL.createObjectURL(data);
			window.location.replace(blob);
			URL.revokeObjectURL(blob);
		});
	});
});
