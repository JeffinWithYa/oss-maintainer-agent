import {StoryConfig} from '@story-protocol/core-sdk'
import {Account, Address, http} from 'viem'
import {privateKeyToAccount} from 'viem/accounts'
const privateKey: Address = '0x${process.env.WALLET_PRIVATE_KEY}'
export const account: Account = privateKeyToAccount(privateKey)

const RPCProviderUrl = 'https://rpc.odyssey.storyrpc.io'
const config: StoryConfig = {
    account:account,
    transport: http(RPCProviderUrl),
    chainId: 'odyssey',
}

export const client = StoryClient.newClient(config)
// export const nftCollectionA = '0x0000000000000000000000000000000000000000'
