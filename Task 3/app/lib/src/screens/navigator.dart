// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../auth.dart';
import '../data.dart';
import '../routing.dart';
import '../screens/sign_in.dart';
import '../widgets/fade_transition_page.dart';
import 'course_details.dart';
import 'assignment_details.dart';
import 'scaffold.dart';

/// Builds the top-level navigator for the app. The pages to display are based
/// on the `routeState` that was parsed by the TemplateRouteParser.
class HackerrankNavigator extends StatefulWidget {
  final GlobalKey<NavigatorState> navigatorKey;

  const HackerrankNavigator({
    required this.navigatorKey,
    super.key,
  });

  @override
  State<HackerrankNavigator> createState() => _HackerrankNavigatorState();
}

class _HackerrankNavigatorState extends State<HackerrankNavigator> {
  final _signInKey = const ValueKey('Sign in');
  final _scaffoldKey = const ValueKey('App scaffold');
  final _assignmentDetailsKey = const ValueKey('Assignment details screen');
  final _courseDetailsKey = const ValueKey('Course details screen');

  @override
  Widget build(BuildContext context) {
    final routeState = RouteStateScope.of(context);
    final authState = HackerrankAuthScope.of(context);
    final pathTemplate = routeState.route.pathTemplate;

    Assignment? selectedBook;
    if (pathTemplate == '/book/:bookId') {
      selectedBook = libraryInstance.allBooks.firstWhereOrNull(
          (b) => b.id.toString() == routeState.route.parameters['bookId']);
    }

    Course? selectedAuthor;
    if (pathTemplate == '/author/:authorId') {
      selectedAuthor = libraryInstance.allAuthors.firstWhereOrNull(
          (b) => b.id.toString() == routeState.route.parameters['authorId']);
    }

    return Navigator(
      key: widget.navigatorKey,
      onPopPage: (route, dynamic result) {
        // When a page that is stacked on top of the scaffold is popped, display
        // the /books or /authors tab in BookstoreScaffold.
        if (route.settings is Page &&
            (route.settings as Page).key == _assignmentDetailsKey) {
          routeState.go('/books/popular');
        }

        if (route.settings is Page &&
            (route.settings as Page).key == _courseDetailsKey) {
          routeState.go('/authors');
        }

        return route.didPop(result);
      },
      pages: [
        if (routeState.route.pathTemplate == '/signin')
          // Display the sign in screen.
          FadeTransitionPage<void>(
            key: _signInKey,
            child: SignInScreen(
              onSignIn: (credentials) async {
                var signedIn = await authState.signIn(
                    credentials.email, credentials.password);
                if (signedIn) {
                  await routeState.go('/books/popular');
                }
                else {
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                    content: Text("Invalid credentials!"),
                  ));
                }
              },
            ),
          )
        else ...[
          // Display the app
          FadeTransitionPage<void>(
            key: _scaffoldKey,
            child: const BookstoreScaffold(),
          ),
          // Add an additional page to the stack if the user is viewing a book
          // or an author
          if (selectedBook != null)
            MaterialPage<void>(
              key: _assignmentDetailsKey,
              child: AssignmentScreen(
                book: selectedBook,
              ),
            )
          else if (selectedAuthor != null)
            MaterialPage<void>(
              key: _courseDetailsKey,
              child: CourseDetailsScreen(
                course: selectedAuthor,
              ),
            ),
        ],
      ],
    );
  }
}
