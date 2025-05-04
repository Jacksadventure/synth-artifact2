function Lottery(id, cover, coverType, width, height, drawPercentCallback) {
    this.conId = id;
    this.conNode = document.getElementById(this.conId);
    this.cover = cover;
    this.coverType = coverType;
    this.background = null;
    this.backCtx = null;
    this.mask = null;
    this.maskCtx = null;
    this.lottery = null;
    this.lotteryType = 'image';
    this.width = width || 300;
    this.height = height || 100;
    this.clientRect = null;
    this.drawPercentCallback = drawPercentCallback;
}