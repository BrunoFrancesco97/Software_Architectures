// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

import '../data/library.dart';
import '../routing.dart';
import '../widgets/course_list.dart';

class CoursesScreen extends StatelessWidget {
  final String title = 'Courses';

  const CoursesScreen({super.key});

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text(title),
        ),
        body: CourseList(
          courses: libraryInstance.allAuthors,
          onTap: (author) {
            RouteStateScope.of(context).go('/author/${author.id}');
          },
        ),
      );
}
