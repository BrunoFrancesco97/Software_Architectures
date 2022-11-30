// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

// api call from button:
// https://stackoverflow.com/questions/50014848/network-request-after-button-click-with-flutter

import 'package:flutter/material.dart';
import 'package:hackerrank/src/data/api_service.dart';
import 'package:url_launcher/link.dart';

import '../data.dart';
import 'course_details.dart';

const List<String> list = <String>['Java', 'C', 'C++', 'Python'];

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
  int count = 0;
  String _currentWeather = "";
  bool apiCall = false; // New variable
  String dropdownValue = list.first;

  void _testAPI() {
    var api = new ApiService();
    api.test().then((weather) {
      setState(() {
        apiCall= false; //Disable Progressbar
        _currentWeather = weather.toString();
      });
    }, onError: (error) {
      setState(() {
        apiCall=false; //Disable Progressbar
        _currentWeather = error.toString();
      });
    });
  }

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
                    children: <Widget> [
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
                                "testo"
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
                          child: Text('Language Code:'),
                        ),
                      ),
                      Center(
                        child : SizedBox(
                            child: DropdownButton<String>(
                              value: dropdownValue,
                              icon: const Icon(Icons.add),
                              elevation: 16,
                              style: const TextStyle(color: Colors.blue),
                              underline: Container(
                                height: 2,
                                color: Colors.blue,
                              ),
                              onChanged: (String? value) {
                                // This is called when the user selects an item.
                                setState(() {
                                  dropdownValue = value!;
                                });
                              },
                              items: list.map<DropdownMenuItem<String>>((String value) {
                                return DropdownMenuItem<String>(
                                  value: value,
                                  child: Text(value),
                                );
                              }).toList(),
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
                            width: 800.0,
                          child: TextField(
                            keyboardType: TextInputType.multiline,
                            maxLines: null,
                            //controller: _textExercise,
                            decoration: InputDecoration(
                                filled: true,
                                //fillColor: Colors.grey,
                                border: OutlineInputBorder(
                                  borderSide: BorderSide.none,
                                  borderRadius: BorderRadius.only(
                                    topLeft: const Radius.circular(13.0),
                                    topRight: const Radius.circular(13.0),
                                  ),
                                ),
                            ),
                          )
                      //constraints: const BoxConstraints(maxWidth: 1000),
                      //width: 800.0,
                      //height: 800.0,
                       /*child: const Card(
                        child: Padding(
                          padding: EdgeInsets.symmetric(vertical: 18, horizontal: 12),
                          child: Text(
                          "-----------------------------------"),
                        ),
                          ),*/
                  ),
                    ),
                      SizedBox(height: 10),
                    Center(
                     child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                        //foregroundColor: Colors.blueGrey,
                        backgroundColor: Colors.blue,
                        padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 15),
                      )/*.copyWith(elevation: ButtonStyleButton.allOrNull(0.0))*/,
                      onPressed: () {
                        setState((){
                          apiCall=true; // Set state like this
                        });
                        if(count == 0){
                          _testAPI();
                          count=count+1;
                        }
                      },
                      child: const Text('Compile'),
                      ),
                    ),
                      SizedBox(height: 10),
                      Center(
                        child: SizedBox(
                          width: 800.0,
                          child: Text('Output:'),
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
                              //child: Text( ""),
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

  Widget getProperWidget(){
    if(apiCall)
      return new CircularProgressIndicator();
    else
      return new Text(
        '$_currentWeather',
        style: Theme.of(context).textTheme.bodyText1,
      );
  }
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
    final ButtonStyle style =
    ElevatedButton.styleFrom(textStyle: const TextStyle(fontSize: 20));

    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          ElevatedButton(
            style: style,
            onPressed: null,
            child: const Text('Disabled'),
          ),
          const SizedBox(height: 30),
          ElevatedButton(
            style: style,
            onPressed: () {},
            child: const Text('Enabled'),
          ),
        ],
      ),
    );
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
              book!.author.name, <---------------
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
