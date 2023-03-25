import JSEncrypt from "jsencrypt";

const publicKey = '-----BEGIN RSA PUBLIC KEY-----MEgCQQClsUgHq/LhJOg/+N4xtJTBNekqlVW60iEK2/MNYzowz7d5Db+Ipkynhhv3qKr7gbDNHvs8kxBh39WZqH4HKC3vAgMBAAE=-----END RSA PUBLIC KEY-----'

export default {
    rsaPublicData(data) {
        let jsEncrypt = new JSEncrypt()
        jsEncrypt.setPublicKey(publicKey)
        return jsEncrypt.encrypt(data)
    }
}
