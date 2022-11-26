// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

import '../data.dart';
import '../routing.dart';
import '../widgets/assignment_list.dart';

class CourseDetailsScreen extends StatelessWidget {
  final Course course;

  const CourseDetailsScreen({
    super.key,
    required this.course,
  });

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text(course.name),
        ),
        body: Center(
          child: Column(
            children: [
              Expanded(
                child: AssignmentList(
                  assignments: course.assignments,
                  onTap: (book) {
                    RouteStateScope.of(context).go('/book/${book.id}');
                  },
                ),
              ),
            ],
          ),
        ),
      );
}
