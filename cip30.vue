<script setup>

module.exports = {
	mounted() {
		this.API = undefined;
		this.pollWallets(0);
	},
	watch: {
		wallets() {
			console.debug("wallets: ", this.wallets);
		},
		activeWallet() {
			console.debug("activeWallet: ", this.activeWallet);
		},
		assets() {
			console.debug("assets: ", this.assets);
		},
		collateral() {
			console.debug("collateral: ", this.collateral);
		},
		address() {
			console.log("address: ", this.address);
		},
		firstAddress() {
			console.log("address: ", this.firstAddress);
		},
		async signTx() {
			console.debug("signTx: ", this.signTx);
			this.witness = await this.API.signTx(this.signTx);
		},
		async signedTx() {
			console.debug("signedTx: ", this.signedTx);
			this.txId = await this.API.submitTx(this.signedTx);
		},
		witness() {
			console.debug("witness: ", this.witness)
		},
		txId() {
			console.log("submitted txId: ", this.txId)
		}
	},
	methods: {
		pollWallets(count = 0) {
			if (window.cardano !== undefined) {
				for (const key in window.cardano) {
					console.log(key);
					if (window.cardano[key].enable && this.wallets.indexOf(key) === -1) {
						this.wallets.push(key);
					}
					console.log(this.wallets)
				}
				this._wallets = window.cardano
				if (this.wallets.length === 0 && count < 3) {
					setTimeout(() => {
						this.pollWallets(count + 1);
					}, 1000);
					return;
				}
			} else {
				this.wallets.push("No wallets found")
			}
		},
		delay(ms) {
			return new Promise(function (resolve) { return setTimeout(resolve, ms); });
		},
		setSignedTx(signedTx) {
			this.signedTx = signedTx;
		},
		async updateValues() {
			while (true) {
				if (this.API !== undefined) {
					this.address = await this.API.getUnusedAddresses();
					this.assets = await this.API.getBalance();
					this.collateral = await this.API.getCollateral("1a004c4b40");
					console.log("querying values")
					await this.delay(5000);
				}
			}
		},
		async setWallet(wallet) {
			this.API = await window.cardano[wallet].enable()
			console.log(Object.getOwnPropertyNames(this.API.experimental))
			await this.updateValues()
		}
	}
};
</script>

<template>
	<div>
		<v-select style="width: 250px" label="Wallets" :items="wallets" @input="setWallet" v-model="activeWallet">
			<template v-slot:item="{ item }">
				<img :src="window.cardano[item].icon" style="width: 32px; height: 32px;" /> {{
					window.cardano[item].name[0].toUpperCase() + window.cardano[item].name.slice(1) }}
			</template>
			<template v-slot:selection="{ item }">
				<img :src="window.cardano[item].icon" style="width: 32px; height: 32px;" />
				<div v-if=firstAddress>{{ firstAddress.slice(0, 10) + "..." + firstAddress.slice(96) }}</div>
				<div v-else=firstAddress>{{ window.cardano[item].name[0].toUpperCase() + window.cardano[item].name.slice(1)
				}}
				</div>
			</template>
		</v-select>
	</div>
</template>
