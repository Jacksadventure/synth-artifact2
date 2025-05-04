const styles = StyleSheet.create({
  icon: {
    width: 24,
    height: 24,
  },
  container: {
    flex: 1,
    width: null,
    height: null,
    resizeMode: 'cover',
    justifyContent: 'flex-start',
    alignItems:'flex-start'
  },
  bigLogoContainer: {
    height: 140, 
    width: 240, 
    backgroundColor:'transparent', 
    flex: 2, 
    justifyContent:'center', 
    alignItems:'center',
    marginLeft: 10
  },
  bigLogo:{
    resizeMode: 'contain', 
    width: 180
  },
  bottomContainer: {
    width:240,
    flex: 2, 
    justifyContent:"flex-end", 
    alignItems:'center',
    backgroundColor: 'transparent', 
    flexDirection:'column'
  },
  weiboItem:{
    width:240, 
    height: 46, 
    flexDirection:'row', 
    backgroundColor:'#00000066', 
    justifyContent:'flex-start',
    alignItems:'center', 
    alignSelf:'flex-end',
    paddingLeft: 40
  }
});