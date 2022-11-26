// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'dart:developer';

import 'package:flutter/widgets.dart';

/// A simple authentication service
class HackerrankAuth extends ChangeNotifier {
  bool _signedIn = false;

  bool get signedIn => _signedIn;

  Future<void> signOut() async {
    await Future<void>.delayed(const Duration(milliseconds: 200));
    // Sign out.
    _signedIn = false;
    notifyListeners();
  }

  Future<bool> signIn(String username, String password) async {
    await Future<void>.delayed(const Duration(milliseconds: 200));

    // Sign in. Allow any password.
    //TODO add API JWT login
    bool state = false;
    if(username=="pino" && password=="pino") {
      state = true;
    }
    log('login as: $username');
    _signedIn = true;
    notifyListeners();
    return state;
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
