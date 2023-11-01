var layerLoadErrorMessages=[];showMessage('Loading',staticTemplates.loadingModal[mode]);
function runGeeViz(){
try{
	Map2.addSerializedLayer({"result": "0", "values": {"1": {"functionInvocationValue": {"functionName": "Feature.bounds", "arguments": {"feature": {"functionInvocationValue": {"functionName": "Feature.buffer", "arguments": {"distance": {"constantValue": 10}, "feature": {"argumentReference": "_MAPPING_VAR_0_0"}}}}}}}, "0": {"functionInvocationValue": {"functionName": "Collection.map", "arguments": {"baseAlgorithm": {"functionDefinitionValue": {"argumentNames": ["_MAPPING_VAR_0_0"], "body": "1"}}, "collection": {"functionInvocationValue": {"functionName": "FeatureCollection.randomPoints", "arguments": {"maxError": {"functionInvocationValue": {"functionName": "ErrorMargin", "arguments": {"value": {"constantValue": 50}}}}, "points": {"constantValue": 500}, "region": {"functionInvocationValue": {"functionName": "GeometryConstructors.Polygon", "arguments": {"coordinates": {"constantValue": [[[-113.21807278537877, 41.786028237932015], [-113.21807278537877, 40.595571243156144], [-111.82280911350377, 40.595571243156144], [-111.82280911350377, 41.786028237932015]]]}, "geodesic": {"constantValue": false}}}}, "seed": {"constantValue": 0}}}}}}}}},{},'Sample',true);
}catch(err){
	layerLoadErrorMessages.push("Error loading: Sample<br>GEE "+err);}
if(layerLoadErrorMessages.length>0){showMessage("Map.addLayer Error List",layerLoadErrorMessages.join("<br>"));}
setTimeout(function(){if(layerLoadErrorMessages.length===0){$('#close-modal-button').click();}}, 2500);
queryWindowMode = "sidePane"
}