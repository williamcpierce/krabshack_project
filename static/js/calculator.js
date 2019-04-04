function calculate() {
	var originSetting = document.getElementById('origin').value;
	var destinationSetting = document.getElementById('destination').value;
	var collateralBox = parseInt(document.getElementById('collateral').value);
	var volumeBox = parseInt(document.getElementById('volume').value);
	var reward = document.getElementById('reward');
	var collateralMult = 0;
	var volumeMult = 0;
	var collateralMax= 0;
	var volumeMax = 0;
	if ((originSetting == "Jita" && destinationSetting == "K3JR-J Astra") || (originSetting == "K3JR-J Astra" && destinationSetting == "Jita")) {
		collateralMult = 0.015;
		volumeMult = 700;
		collateralMax= 20000000000;
		volumeMax = 320000;
	}
	if ((originSetting == "Jita" && destinationSetting == "K3JR-J NPC") || (originSetting == "K3JR-J NPC" && destinationSetting == "Jita")) {
		collateralMult = 0.02;
		volumeMult = 0;
		collateralMax= 20000000000;
		volumeMax = 400;
	}
	if ((originSetting == "K3JR-J NPC" && destinationSetting == "K3JR-J Astra") || (originSetting == "K3JR-J Astra" && destinationSetting == "K3JR-J NPC")) {
		collateralMult = 0.005;
		volumeMult = 0;
		collateralMax= 20000000000;
		volumeMax = 400;
	}
	var myReward = (collateralBox * collateralMult) + (volumeBox * volumeMult);
	var myRewardInt = float2int(myReward);
	reward.value = numberWithCommas(myRewardInt);
};

function float2int(value) {
	return value | 0;
};

function numberWithCommas(value) {
	return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

function clipboardCopy() {
	var copyText = document.getElementById("reward");
	copyText.select();
	document.execCommand("copy");
};

$(document).ready(function() {
	$('#rewardcopy').tooltip({
		title: "Copied!",
		trigger: "click"
	});
});
