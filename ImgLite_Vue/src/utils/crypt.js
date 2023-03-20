import JSEncrypt from "jsencrypt";

const publicKey = '-----BEGIN RSA PUBLIC KEY-----MEgCQQC0EFaB7ZryMQj17WV6W2KbQturkT038Ux95d7PYFWkIoFaD5qYeleMuwrd7/y+FsvnaJKcQwuNMNoTa7+G3w39AgMBAAE=-----END RSA PUBLIC KEY-----'

export default {
    rsaPublicData(data) {
        let jsEncrypt = new JSEncrypt()
        jsEncrypt.setPublicKey(publicKey)
        return jsEncrypt.encrypt(data)
    }
}
