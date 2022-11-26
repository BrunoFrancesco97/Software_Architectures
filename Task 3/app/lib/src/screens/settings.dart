// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';
import 'package:url_launcher/link.dart';

import '../auth.dart';
import '../routing.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  @override
  Widget build(BuildContext context) => Scaffold(
        body: SafeArea(
          child: SingleChildScrollView(
            child: Align(
              alignment: Alignment.topCenter,
              child: SizedBox/*ConstrainedBox*/(
                //constraints: const BoxConstraints(maxWidth: 1000),
                width: 500.0,
                height: 200.0,
                child: const Card(
                  child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                    child: SettingsContent(),
                  ),
                ),
              ),
            ),
          ),
        ),
      );
}

class SettingsContent extends StatelessWidget {
  const SettingsContent({
    super.key,
  });

  @override
  Widget build(BuildContext context) => /*Card(
    //color: Colors.grey,
    child:*/
  Column(children: [
    //...[
    Text(
    'Account',
    style: Theme.of(context).textTheme.headlineSmall,
  ),
    Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: const [

                SizedBox(height: 10),
                Text('Surname:'),
                SizedBox(height: 10),
                Text('Email:'),
                SizedBox(height: 10),
                Text('Role:'),
              ],
            ),
          ),
        ),
        Flexible(
          fit: FlexFit.tight,
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: const [
                Text(
                  '+100', //testo db
                  maxLines: 1,
                  softWrap: false,
                  overflow: TextOverflow.fade,
                ),
                SizedBox(height: 10),
                Text(
                  '18 Sept 2021', //testo db
                  maxLines: 1,
                  softWrap: false,
                  overflow: TextOverflow.fade,
                ),
                SizedBox(height: 10),
                Text(
                  '18 Sept 2021', //testo db
                  maxLines: 1,
                  softWrap: false,
                  overflow: TextOverflow.fade,
                ),
                SizedBox(height: 10),
                Text(
                  '18 Sept 2021', //testo db
                  maxLines: 1,
                  softWrap: false,
                  overflow: TextOverflow.fade,
                ),
              ],
            ),
          ),
        ),
      ],
    ),
    ],
  );




















      /*Column(
        children: [
          ...[
            Text(
              'Account',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            /*ElevatedButton(
              onPressed: () {
                HackerrankAuthScope.of(context).signOut();
              },
              child: const Text('Sign out'),
            ),*/
            Text/*Link*/(
                'Name',
                style: Theme.of(context).textTheme.headlineSmall,
              /*uri: Uri.parse('/book/0'),
              builder: (context, followLink) => TextButton(
                onPressed: followLink,
                child: const Text('Go directly to /book/0 (Link)'),*/
              ),
            Text(
              'Surname',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            Text(
              'email',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            Text(
              'role',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            //),
            /*TextButton(
              child: const Text('Go directly to /book/0 (RouteState)'),
              onPressed: () {
                RouteStateScope.of(context).go('/book/0');
              },
            ),*/
          ].map((w) => Padding(padding: const EdgeInsets.all(8), child: w)),
          /*TextButton(
            onPressed: () => showDialog<String>(
              context: context,
              builder: (context) => AlertDialog(
                title: const Text('Alert!'),
                content: const Text('The alert description goes here.'),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context, 'Cancel'),
                    child: const Text('Cancel'),
                  ),
                  TextButton(
                    onPressed: () => Navigator.pop(context, 'OK'),
                    child: const Text('OK'),
                  ),
                ],
              ),
            ),
            child: const Text('Show Dialog'),
          )*/
        ],
      );*/
}
