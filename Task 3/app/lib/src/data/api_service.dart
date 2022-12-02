import 'dart:developer';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'dart:convert';

import 'course.dart';
import 'assignment.dart';
import 'constants.dart';

import 'package:dio_cookie_manager/dio_cookie_manager.dart';
import 'package:cookie_jar/cookie_jar.dart';

class ApiService {
  static bool isLogged = false;
  static var mail;
  static var password;
  static var encryptedCredentials;
  static var cookieJar = CookieJar();
  static Dio? _api;/* = Dio(
    BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: 5000,
      receiveTimeout: 3000
    )
  );*/

  //method for getting dio instance
  static Dio? getInstance() {
    if (_api == null) {
      _api = createDioInstance();
    }
    return _api;
  }

  static Dio createDioInstance() {
    var dio = Dio();
    // adding interceptor
    dio.interceptors.clear();
    if(!kIsWeb) {
      dio.interceptors.add(CookieManager(cookieJar));
    }
    log("created");
    dio.get(
      ApiConstants.baseUrl + ApiConstants.login,
        options: Options(
          headers: {
            "Authorization": "Basic "+encryptedCredentials,
            "Accept" : "*/*"
            //"Access-Control-Allow-Origin": "http://localhost"
        }
        )
    );

    /*
    dio.interceptors.add(InterceptorsWrapper(onRequest: (options, handler) {
      return handler.next(options);//modify your request
    }, onResponse: (response, handler) {
      if (response != null) {//on success it is getting called here
        return handler.next(response);
      } else {
        return null;
      }
    }, onError: (DioError e, handler) async {

      if (e.response != null) {
        if (e.response?.statusCode == 401) {//catch the 401 here
          dio.interceptors.requestLock.lock();
          dio.interceptors.responseLock.lock();
          RequestOptions requestOptions = e.requestOptions;

          //Repository repository = Repository();
          //var accessToken = await repository.readData("accessToken");
          final opts = new Options(method: requestOptions.method);
          dio.options.headers["Authorization"] = "Basic " + encryptedCredentials;
          dio.options.headers["Accept"] = "*/
    /*";
          dio.interceptors.requestLock.unlock();
          dio.interceptors.responseLock.unlock();
          final response = await dio.request(requestOptions.path,
              options: opts,
              cancelToken: requestOptions.cancelToken,
              onReceiveProgress: requestOptions.onReceiveProgress,
              data: requestOptions.data,
              queryParameters: requestOptions.queryParameters);
          if (response != null) {
            handler.resolve(response);
          } else {
            return null;
          }
        } else {
          handler.next(e);
        }
      }

    }));*/
    return dio;
  }

  static void setCredentials(mail, password) {
    mail=mail;
    password=password;
    Codec<String, String> stringToBase64 = utf8.fuse(base64);
    encryptedCredentials =  stringToBase64.encode(mail+":"+password);
  }

  Future login() async {
    Codec<String, String> stringToBase64 = utf8.fuse(base64);
    String encoded_credentials =  stringToBase64.encode(mail+":"+password);
    try {
      var response = await _api?.get(
          ApiConstants.login,
        options: Options(
          headers: {
            "Authorization": "Basic "+encoded_credentials
          }
        )
      );
      if(response != null) {
        log(response.toString());
        log(response.statusCode.toString());
        if (response.statusCode == 200)
          return true;
      }
    } catch (e) {
      log(e.toString());
    }
  }

  static void logout() async {
    try {
      var response = await _api?.get(
          ApiConstants.baseUrl + ApiConstants.logout
      );
      if(response != null) {
        log(response.toString());
        log(response.statusCode.toString());
        if (response.statusCode == 200)
          _api=null;
          return;
      }
    } catch (e) {
      log(e.toString());
    }
  }

  static String getEncodedCredentials() {
    return encryptedCredentials;
  }

  Future test() async {
    //sleep(Duration(seconds: 1));
    log("test api call");
    return "test";
  }
}