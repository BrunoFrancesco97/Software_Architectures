import 'dart:convert';
import 'dart:developer';

import 'package:dio/dio.dart';

import '../data.dart';
import 'api_service.dart';

class ApiWrapper {
  static Dio? api;

  Future<bool> login(String username, String password) async {
    log("[ApiWrapper] login call");
    Codec<String, String> stringToBase64 = utf8.fuse(base64);
    String encoded_credentials =  stringToBase64.encode(username+":"+password);
    try {
      var response = await Dio().get(
          ApiConstants.baseUrl + ApiConstants.login,
          options: Options(
              headers: {
                "Authorization": "Basic "+encoded_credentials
              }
          )
      );
      log("[Api Wrapper] getted response");
      if(response != null) {
        if (response.statusCode == 200) {
          log("[ApiWrapper] login passed");
          ApiService.setCredentials(username, password);
          api = ApiService.getInstance();
          /*api?.get(
            ApiConstants.baseUrl + ApiConstants.logout
          );*/
          return true;
        }
        log("[ApiWrapper] login failed");
        return false;
      }
    } catch (e) {
      log(e.toString());
    }
    /*
    var response = await login_dio_check.get(
      ApiConstants.baseUrl + ApiConstants.login,
      options: Options(
        headers: {
          "Authorization": "Basic "+encoded_credentials
        }
      )
    );
    */

    /*var response = await api?.get(
        ApiConstants.baseUrl + ApiConstants.login,
        options: Options(
            headers: {
              "Authorization": "Basic "+encoded_credentials
            }
        )
    );*/
    return false;
  }

  Future<bool> logout() async {
    bool ok = false;
    /*var result=api?.get(
      ApiConstants.baseUrl + ApiConstants.logout
    );*/

    /*var response = await api?.get(
        ApiConstants.baseUrl + ApiConstants.logout
    );*/

    log("[API WRAPPER] jwt"+ApiService.getEncodedCredentials());
    //api = ApiService.getInstance();
    ApiService.logout();
    /*if(result != null) {
      if(result == 200) {
        ok = true;
      }
    }*/
    return ok;

    /*


      static Future<bool> logout() async {
    var response = _api?.get(
      ApiConstants.baseUrl + ApiConstants.logout
    );
    _api?.interceptors.clear();
    _api = null;
    /*if(response != null) {
      if (response.statuscode == true) {
        _api?.interceptors.clear();
        _api = null;
      }
    }
    return await response;*/
    return true;
  }
     */
  }
}