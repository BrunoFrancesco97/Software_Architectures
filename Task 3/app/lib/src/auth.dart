// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'dart:convert';
import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:flutter/widgets.dart';
//import 'package:hackerrank/src/data/api_service.dart';
import 'package:hackerrank/src/data/api_wrapper.dart';
import 'data.dart';

/// A simple authentication service
class HackerrankAuth extends ChangeNotifier {
  ApiWrapper api = ApiWrapper();

  bool _signedIn = false;

  bool get signedIn => _signedIn;

  Future<void> signOut() async {
    await Future<void>.delayed(const Duration(milliseconds: 200));
    // Sign out.
    await api.logout();
    _signedIn = false;
    notifyListeners();
  }

  Future<bool> signIn(String username, String password) async {
    await Future<void>.delayed(const Duration(milliseconds: 200));

    bool result = false;
    try {
      result = await api.login(username, password);
      if(result == true) {
        log("[AUTH] login successful");
      }
      else {
        log("[AUTH] login denied");
      }
    } catch (e) {
      log("[AUTH ERROR] "+e.toString());
    }
    _signedIn = result;
    notifyListeners();

    return result;
      //Codec<String, String> stringToBase64 = utf8.fuse(base64);
      //String encoded_credentials =  stringToBase64.encode(username+":"+password);
      //var r = await api.login(username, password);
      log("[AUTH] login call..");


      /*
      var response = await Dio().get(
          ApiConstants.baseUrl + ApiConstants.login,
          options: Options(
              headers: {
                "Authorization": "Basic "+encoded_credentials
              }
          )
      );
      log(response.toString());
      if(response.statusCode==200) {
        result = true;
      }

    } catch (e) {
      log("[AUTH ERROR]"+e.toString());
    }
    return result;
    */

    /*ApiService.setCredentials(username, password);
    Dio? api = ApiService.getInstance();
    log(api.toString());
    log(api.hashCode.toString());*/

    //api.get()


    // Sign in. Allow any password.
    //TODO add API JWT login
    /*bool state = false;
    try {
      var result = api.login(username, password);
      if(await result == true) {
        state = true;
      }
      /*Codec<String, String> stringToBase64 = utf8.fuse(base64);
      String encoded_credentials =  stringToBase64.encode(username+":"+password);
      //var r = await api.login(username, password);
      log("login call..");
      var response = await api?.get(
          ApiConstants.baseUrl + ApiConstants.login,
          options: Options(
              headers: {
                "Authorization": "Basic "+encoded_credentials
              }
          )
      );
      state = false;
      log(response.toString());

      response = await api?.get(
          ApiConstants.baseUrl + ApiConstants.logout
      );*/
    } catch (e) {
      log("[AUTH ERROR]"+e.toString());
      state = false;
    }
    /*if(username=="pino" && password=="pino") {
      state = true;
    }*/
    log('login as: $username');
    _signedIn = state;
    notifyListeners();
    return state;*/
  }

  @override
  bool operator ==(Object other) =>
      other is HackerrankAuth && other._signedIn == _signedIn;

  @override
  int get hashCode => _signedIn.hashCode;
}

class HackerrankAuthScope extends InheritedNotifier<HackerrankAuth> {
  const HackerrankAuthScope({
    required super.notifier,
    required super.child,
    super.key,
  });

  static HackerrankAuth of(BuildContext context) => context
      .dependOnInheritedWidgetOfExactType<HackerrankAuthScope>()!
      .notifier!;
}
