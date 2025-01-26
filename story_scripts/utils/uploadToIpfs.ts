const pinataSDK = require('@pinata/sdk')
const pinata = new pinataSDK({pinataJWT: process.env.PINATA_JWT})

export async function uploadJSONToIpfs(jsonMetadata: any): Promise<string> {
    const {IpfsHash} = await pinata.pinJSONToIPFS(jsonMetadata):
    return IpfsHash
}


