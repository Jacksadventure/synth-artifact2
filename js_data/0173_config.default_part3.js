// 数据库配置信息。
exports.sequelize = {
  dialect: 'mysql',   // 数据库类型，支持 mysql，sqlite,mssql,pgsql,oracle。
  host: "localhost",  // 数据库服务器地址。
  port: 3306, // 数据库连接端口号。
  database: "user", // 数据库名称。
  username: "root",   // 数据库登录用户名。
  password: "1234567890",   // 数据库登录密码。
  define: {
      freezeTableName: true, // Model 对应的表名将与model名相同。
      timestamps: false // 默认情况下，Sequelize会将createdAt和updatedAt的属性添加到模型中，以便您可以知道数据库条目何时进入数据库以及何时被更新（ 确实是太方便了，然而我们一般用不到 ....）。
  }
};