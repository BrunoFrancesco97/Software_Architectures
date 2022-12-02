// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

import '../data.dart';
import '../routing.dart';
import '../widgets/assignment_list.dart';

class AssignmentsScreen extends StatefulWidget {
  const AssignmentsScreen({
    super.key,
  });

  @override
  State<AssignmentsScreen> createState() => _AssignmentsScreenState();
}

class _AssignmentsScreenState extends State<AssignmentsScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this)
      ..addListener(_handleTabIndexChanged);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    final newPath = _routeState.route.pathTemplate;
    if/* (newPath.startsWith('/books/popular')) {
      _tabController.index = 0;
    } else if*/ (newPath.startsWith('/books/new')) {
      _tabController.index = 1;
    } else if (newPath == '/books/all') {
      _tabController.index = 2;
    }
  }

  @override
  void dispose() {
    _tabController.removeListener(_handleTabIndexChanged);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: const Text('Assignments'),
          bottom: TabBar(
            controller: _tabController,
            tabs: const [
              /*Tab(
                text: 'Popular',
                icon: Icon(Icons.people),
              ),*/
              Tab(
                text: 'ToDo',
                icon: Icon(Icons.new_releases),
              ),
              Tab(
                text: 'Done',
                icon: Icon(Icons.list),
              ),
            ],
          ),
        ),
        body: TabBarView(
          controller: _tabController,
          children: [
            /*BookList(
              books: libraryInstance.popularBooks,
              onTap: _handleBookTapped,
            ),*/
            AssignmentList(
              assignments: libraryInstance.newBooks,
              onTap: _handleBookTapped,
            ),
            AssignmentList(
              assignments: libraryInstance.allBooks,
              onTap: _handleBookTapped,
            ),
          ],
        ),
      );

  RouteState get _routeState => RouteStateScope.of(context);

  void _handleBookTapped(Assignment book) {
    _routeState.go('/book/${book.id}');
  }

  void _handleTabIndexChanged() {
    switch (_tabController.index) {
      case 1:
        _routeState.go('/books/new');
        break;
      case 2:
        _routeState.go('/books/all');
        break;
      /*case 0:*/
      default:
        /*_routeState.go('/books/popular');*/
        _routeState.go('/books/new');
        break;
    }
  }
}
