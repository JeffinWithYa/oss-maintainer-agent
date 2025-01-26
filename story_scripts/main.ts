import dotenv from 'dotenv'
import OpenAI from 'openai'
import { uploadJSONToIpfs } from './utils/uploadToIpfs'
dotenv.config()

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
})

async function main() {
    const image = await openai.images.generate({
        model: 'dall-e-3',
        prompt: 'A beautiful image of a cat',
        size: '1024x1024',
    })
    console.log(image.data)

    const ipMetadata: IpMetadata = client.ipAsset.generateIpMetadata({
        title: 'DALL-E Image',
        description: 'This is a DALL-E image',
        ipType: 'image',
        attributes: [
            {key: 'Model', value: 'DALL-E 3'},
            {key: 'Prompt', value: 'A beautiful image of a cat'},

        ],
        creators: [{
            name:'Security Agent',
            contributionPercent: 100,
            address: account.address,
        }],
        
    })

const nftMetadata = {
    name: 'NFT representing ownership of our image',
    description: 'This is a NFT representing ownership of our image',
    image: image.data[0].url,
    attributes: [
        {key: 'Model', value: 'DALL-E 3'},
        {key: 'Prompt', value: 'A beautiful image of a cat'},
    ],
}

const ipIpfsHash = await uploadJSONToIpfs(ipMetadata);
const ipHash = createHash('sha256').update(JSON.stringify(ipMetadata)).digest('hex');
const nftIpfsHash = await uploadJSONToIpfs(nftMetadata);
const nftHash = createHash('sha256').update(JSON.stringify(ipMetadata)).digest('hex');

const response = await client.ipAsset.mintAndRegisterIpAssetWithPilTerms({
    spgNftContract: nftCollectionAddress,
    pilType: PIL_TYPE.NON_COMMERCIAL_REMIX,
    ipMetadata: {
        ipMetadataURI: `https://ipfs.io/ipfs/${ipIpfsHash}`,
        nftMetadataURI: `https://ipfs.io/ipfs/${nftIpfsHash}`,
        ipMetadataHash: `0x${ipHash}`,
        nftMetadataHash: `0x${nftHash}`,
    }
    txOptions: {
        waitForTransaction: true,
    },
})
console.log(response)

}

main()
