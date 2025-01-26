async function main() {
    const newCollection = await client.nftClient.createNFTCollection({
        name: 'DALL-E NFTs',
        symbol: 'DALLE',
        isPublicMinting: true,
        mintFeeRecipient:zeroAddress,
        contractURI:'',
        txOptions: {
            waitForTransaction: true,
        },
        

    })
    console.log(newCollection)
}

main()
