/*
 * @datastructure 用户信息模型
 * @attribute openid:String (tbd)
 * @attribute aliyas:String 微信昵称(微信新版接口改为手动输入，我还没更新)
 * @attribute avatarUrl:String 用户头像URL地址(新版本接口为自选上传)
 * @attribute name:String 用户所输入的真实姓名
 */

export class User {
    constructor() {
        //this.openid = ''
        this.aliyas = ''
        this.avatarUrl = ''
        this.name = ''
    }

    // 存储用户输入信息
    get storgeUserInfoSync() {
        if (this) {
            wx.removeStorageSync('user')
            wx.setStorageSync('user', this)
        }
    }
    get changeName() {
        const iUser = wx.getStorageSync('user')
        iUser.name = this.name
        wx.removeStorageSync('user')
        wx.setStorageSync('user', iUser)
    }
}