// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';
import 'package:url_launcher/link.dart';

import '../data.dart';
import 'course_details.dart';

class AssignmentScreen extends StatefulWidget {
  final Assignment? book;
  const AssignmentScreen({
    super.key,
    this.book
  });

  @override
  State<AssignmentScreen> createState() => _AssignmentScreenState();

}

class _AssignmentScreenState extends State<AssignmentScreen> {
  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
           title: Text("titolo assignment"), //<- titolo assignment
        ),
        body: SafeArea(
            child: SingleChildScrollView(
              child: Align(
                  alignment: Alignment.center,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: const [
                      Center(
                        child: Text(
                          "titolo assignment",
                          style: TextStyle(fontSize: 30),/*Theme.of(context).textTheme.headlineSmall*/
                        ),
                      ),
                      Center(
                        child: SizedBox(
                  //constraints: const BoxConstraints(maxWidth: 1000),
                          width: 800.0,
                          //height: 200.0,//double.infinity,
                          child: const Card(
                            child: Padding(
                              padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                              //child: BookDetailsScreen(
                                //book: selectedBook,
                              child: Text(
                                "-----------------------------------"
                                    "----------------------------------"
                                    "....................................................."
                                    "...................................................."
                                    "......................................................."
                                    ".............prova............................"
                                    "..................................."
                                    "....................................................."
                                    ".......................................................................""....................................................."
                                    "...................................................."
                                    "......................................................."
                                    "..............................................."
                                    "..................................."
                                    "....................................................."
                                    "......................................................................."
                                    "....................................................."
                                    "...................................................."
                                    "......................................................."
                                    "..............................................."
                                    "..................................."
                                    "....................................................."
                                    "......................................................................."
                                    "....................................................."
                                    "...................................................."
                                    "......................................................."
                                    "..............................................."
                                    "..................................."
                                    "....................................................."
                                    "..............1213........................................................."
                              )
                            //),
                          ),
                        ),
                      ),
                      ),
                      SizedBox(height: 10),
                      Center(
                        child: SizedBox(
                          width: 800.0,
                           child: Text('Code:'),
                        ),
                      ),
                      SizedBox(height: 10),
                    Center(
                    child: SizedBox(
                      //constraints: const BoxConstraints(maxWidth: 1000),
                      width: 800.0,
                      //height: 800.0,
                       child: const Card(
                        child: Padding(
                          padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                          child: Text(
                          "-----------------------------------"),
                        ),
                          ),
                  ),
                    ),
                      Center(
                        child: SizedBox(
                          //constraints: const BoxConstraints(maxWidth: 1000),
                          width: 800.0,
                          //height: 800.0,
                          child: const Card(
                            child: Padding(
                              padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                              child: Text( ""),
                            ),
                          ),
                        ),
                      ),
                ],
              )
            ),

        ),
        ),
  );
}


class BookDetailsScreen extends StatelessWidget {
  final Assignment? book;

  const BookDetailsScreen({
    super.key,
    this.book,
  });

  @override
  Widget build(BuildContext context) {
    if (book == null) {
      return const Scaffold(
        body: Center(
          child: Text('No book found.'),
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(
        title: Text("titolo assignment"), //<- titolo assignment
      ),
      body: Center(
        child: Column(
          children: [
            Text(
              "titolo assignment",
              style: Theme.of(context).textTheme.headlineSmall,
            ),
             SafeArea(
              child: SingleChildScrollView(
                child: Align(
                  alignment: Alignment.topCenter,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        SizedBox(
                          //constraints: const BoxConstraints(maxWidth: 1000),
                          width: 500.0,
                          height: 200.0,
                          child: const Card(
                            child: Padding(
                              padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                              child: BookDetailsScreen(),
                            ),
                          ),
                        ),
                        Text('Surname:'),
                        SizedBox(
                          //constraints: const BoxConstraints(maxWidth: 1000),
                          width: 800.0,
                          height: 800.0,
                          child: const Card(
                            child: Padding(
                              padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                              child: BookDetailsScreen(),
                            ),
                          ),
                        ),
                      ],
                    )
                ),
              ),
            ),
            /*ConstrainedBox (
              //constraints: const BoxConstraints(maxWidth: 1000),
              constraints: BoxConstraints.expand(height: 200, width: 200),
            )*/

            /*Text(
              book!.author.name,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            TextButton(
              child: const Text('View author (Push)'),
              onPressed: () {
                Navigator.of(context).push<void>(
                  MaterialPageRoute<void>(
                    builder: (context) =>
                        AuthorDetailsScreen(author: book!.author),
                  ),
                );
              },
            ),
            Link(
              uri: Uri.parse('/author/${book!.author.id}'),
              builder: (context, followLink) => TextButton(
                onPressed: followLink,
                child: const Text('View author (Link)'),
              ),
            ),*/
          ],
        ),
      ),
    );
  }
}
