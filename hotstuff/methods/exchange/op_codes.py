"""Exchange operation codes."""
EXCHANGE_OP_CODES = {
    # Account Actions
    "addAgent": 1201,
    "revokeAgent": 1211,
    "updatePerpInstrumentLeverage": 1203,
    "approveBrokerFee": 1207,
    "createReferralCode": 1208,
    "setReferrer": 1209,
    "claimReferralRewards": 1210,

    # Trading Actions
    "placeOrder": 1301,
    "cancelByOid": 1302,
    "cancelAll": 1311,
    "cancelByCloid": 1312,

    # Collateral Actions
    "accountSpotWithdrawRequest": 1002,
    "accountDerivativeWithdrawRequest": 1003,
    "accountSpotBalanceTransferRequest": 1051,
    "accountDerivativeBalanceTransferRequest": 1052,
    "accountInternalBalanceTransferRequest": 1053,

    # Vault Actions
    "depositToVault": 1401,
    "redeemFromVault": 1402,
}
