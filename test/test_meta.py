# -*- coding: utf-8 -*-

"""Test module “meta.py”."""


import unittest
import mscxyz
from mscxyz.meta import MetaTag, Meta, Vbox, Combined, distribute_field, \
                        UnifedInterface
from mscxyz.tree import Tree
import helper


class TestFunctionDistributeField(unittest.TestCase):

    def test_simple(self):
        match = distribute_field('We are the champions - Queen',
                                 '$title - $composer')
        self.assertEqual(match, {'composer': 'Queen', 'title':
                         'We are the champions'})


class TestClassUnifiedInterface(unittest.TestCase):

    def setUp(self):
        self.fields = [
            'combined_composer',
            'combined_lyricist',
            'combined_subtitle',
            'combined_title',
            'metatag_arranger',
            'metatag_composer',
            'metatag_copyright',
            'metatag_creation_date',
            'metatag_lyricist',
            'metatag_movement_number',
            'metatag_movement_title',
            'metatag_platform',
            'metatag_poet',
            'metatag_source',
            'metatag_translator',
            'metatag_work_number',
            'metatag_work_title',
            'vbox_composer',
            'vbox_lyricist',
            'vbox_subtitle',
            'vbox_title',
        ]

    def _init_class(self, filename):
        tmp = helper.get_tmpfile_path(filename)
        tree = Tree(tmp)
        interface = UnifedInterface(tree.root)
        return interface, tree, tmp

    def test_subclasses(self):
        interface, tree, tmp = self._init_class('simple.mscx')
        self.assertTrue(interface.metatag)
        self.assertTrue(interface.vbox)
        self.assertTrue(interface.combined)

    def test_static_method_split(self):
        result = UnifedInterface._split('metatag_work_title')
        self.assertEqual(result, {'field': 'work_title', 'object': 'metatag'})
        with self.assertRaises(ValueError):
            UnifedInterface._split('metatag')
        with self.assertRaises(ValueError):
            UnifedInterface._split('lol_work_title')

    def test_get_simple(self):
        interface, tree, tmp = self._init_class('simple.mscx')
        self.assertEqual(interface.vbox_title, 'Title')
        self.assertEqual(interface.metatag_work_title, 'Title')

    def test_get_all_values(self):
        interface, tree, tmp = self._init_class('meta-all-values.mscx')

        self.assertEqual(interface.combined_composer, 'vbox_composer')
        self.assertEqual(interface.combined_lyricist, 'vbox_lyricist')
        self.assertEqual(interface.combined_subtitle, 'vbox_subtitle')
        self.assertEqual(interface.combined_title, 'vbox_title')

        for field in self.fields[4:]:
            self.assertEqual(getattr(interface, field), field)

    def test_set_all_values(self):
        interface, tree, tmp = self._init_class('meta-all-values.mscx')

        for field in self.fields:
            setattr(interface, field, field + '_test')
            self.assertEqual(getattr(interface, field), field + '_test')

        tree.save()
        tree = Tree(tmp)
        interface = UnifedInterface(tree.root)

        self.assertEqual(interface.combined_composer, 'vbox_composer_test')
        self.assertEqual(interface.combined_lyricist, 'vbox_lyricist_test')
        self.assertEqual(interface.combined_subtitle, 'vbox_subtitle_test')
        self.assertEqual(interface.combined_title, 'vbox_title_test')

        for field in self.fields[4:]:
            self.assertEqual(getattr(interface, field), field + '_test')

    def test_method_get_all_fields(self):
        fields = UnifedInterface.get_all_fields()
        self.assertEqual(fields, self.fields)

    def test_method_export_to_dict(self):
        interface, tree, tmp = self._init_class('meta-all-values.mscx')
        result = interface.export_to_dict()
        self.assertEqual(result, {
            'combined_composer': 'vbox_composer',
            'combined_lyricist': 'vbox_lyricist',
            'combined_subtitle': 'vbox_subtitle',
            'combined_title': 'vbox_title',
            'metatag_arranger': 'metatag_arranger',
            'metatag_composer': 'metatag_composer',
            'metatag_copyright': 'metatag_copyright',
            'metatag_creation_date': 'metatag_creation_date',
            'metatag_lyricist': 'metatag_lyricist',
            'metatag_movement_number': 'metatag_movement_number',
            'metatag_movement_title': 'metatag_movement_title',
            'metatag_platform': 'metatag_platform',
            'metatag_poet': 'metatag_poet',
            'metatag_source': 'metatag_source',
            'metatag_translator': 'metatag_translator',
            'metatag_work_number': 'metatag_work_number',
            'metatag_work_title': 'metatag_work_title',
            'vbox_composer': 'vbox_composer',
            'vbox_lyricist': 'vbox_lyricist',
            'vbox_subtitle': 'vbox_subtitle',
            'vbox_title': 'vbox_title',
        })

    def test_attribute_fields(self):
        interface, tree, tmp = self._init_class('meta-all-values.mscx')
        self.assertEqual(interface.fields, self.fields)


class TestClassMeta(unittest.TestCase):

    def setUp(self):
        self.meta = Meta(helper.get_tmpfile_path('simple.mscx'))

    def test_show(self):
        with helper.Capturing() as output:
            mscxyz.execute(['meta', '-s',
                           helper.get_tmpfile_path('simple.mscx')])

        compare = [
            '',
            '\x1b[31msimple.mscx\x1b[0m',
            '\x1b[34mfilename\x1b[0m: simple',
            '\x1b[33mworkTitle\x1b[0m: Title',
            '\x1b[33mplatform\x1b[0m: Linux',
            '\x1b[33mcomposer\x1b[0m: Composer',
            '\x1b[32mComposer\x1b[0m: Composer',
            '\x1b[32mTitle\x1b[0m: Title'
        ]

        self.assertTrue('\x1b[33mworkTitle\x1b[0m: Title' in output)
        self.assertEqual(output.sort(), compare.sort())


class TestClassMetaTag(unittest.TestCase):

    def _init_class(self, filename):
        tmp = helper.get_tmpfile_path(filename)
        tree = Tree(tmp)
        meta = MetaTag(tree.root)
        return meta, tree, tmp

    def test_static_method_to_camel_case(self):
        camel_case = MetaTag._to_camel_case
        self.assertEqual(camel_case('work_title'), 'workTitle')
        self.assertEqual(camel_case('composer'), 'composer')
        self.assertEqual(camel_case('work_title_lol'), 'workTitleLol')
        self.assertEqual(camel_case('workTitle'), 'workTitle')

    def test_get(self):
        meta, tree, tmp = self._init_class('simple.mscx')
        self.assertEqual(meta.workTitle, 'Title')
        self.assertEqual(meta.work_title, 'Title')
        self.assertEqual(meta.arranger, None)
        self.assertEqual(meta.composer, 'Composer')

    def test_set(self):
        meta, tree, tmp = self._init_class('simple.mscx')
        meta.workTitle = 'WT'
        meta.movement_title = 'MT'
        tree.save()
        tree = Tree(tmp)
        meta = MetaTag(tree.root)
        self.assertEqual(meta.work_title, 'WT')
        self.assertEqual(meta.movementTitle, 'MT')
        xml_string = helper.read_file(tmp)
        self.assertTrue('<metaTag name="workTitle">WT</metaTag>' in
                        xml_string)

    def test_get_exception(self):
        meta, tree, tmp = self._init_class('simple.mscx')
        with self.assertRaises(AttributeError):
            meta.lol

    def test_set_exception(self):
        meta, tree, tmp = self._init_class('simple.mscx')
        with self.assertRaises(AttributeError):
            meta.lol = 'lol'

    def test_clean(self):
        meta, tree, tmp = self._init_class('simple.mscx')
        meta.arranger = 'A'
        self.assertEqual(meta.arranger, 'A')
        meta.clean()
        self.assertEqual(meta.arranger, '')


class TestClassVbox(unittest.TestCase):

    def _init_class(self, filename):
        tmp = helper.get_tmpfile_path(filename)
        tree = Tree(tmp)
        vbox = Vbox(tree.root)
        return vbox, tree, tmp

    def test_init(self):
        vbox, tree, tmp = self._init_class('no-vbox.mscx')
        tree.save()
        xml_string = helper.read_file(tmp)
        self.assertTrue('<VBox>' in xml_string)

    def test_get(self):
        vbox, tree, tmp = self._init_class('simple.mscx')
        self.assertEqual(vbox.Title, 'Title')
        self.assertEqual(vbox.Composer, 'Composer')
        self.assertEqual(vbox.Subtitle, None)
        self.assertEqual(vbox.title, 'Title')
        self.assertEqual(vbox.composer, 'Composer')

    def test_get_exception(self):
        vbox, tree, tmp = self._init_class('simple.mscx')
        with self.assertRaises(AttributeError):
            vbox.lol

    def _assert_set(self, filename):
        tmp = helper.get_tmpfile_path(filename)
        tree = Tree(tmp)
        vbox = Vbox(tree.root)
        vbox.Title = 'lol'
        vbox.composer = 'lol'
        tree.save()
        tree = Tree(tmp)
        vbox = Vbox(tree.root)
        self.assertEqual(vbox.title, 'lol')
        self.assertEqual(vbox.Composer, 'lol')
        xml_string = helper.read_file(tmp)
        self.assertTrue('<text>lol</text>' in xml_string)

    def test_set_with_existing_vbox(self):
        self._assert_set('simple.mscx')

    def test_set_no_inital_vbox(self):
        self._assert_set('no-vbox.mscx')

    def test_set_exception(self):
        vbox, tree, tmp = self._init_class('simple.mscx')
        with self.assertRaises(AttributeError):
            vbox.lol = 'lol'


class TestClassCombined(unittest.TestCase):

    def _init_class(self, filename):
        tmp = helper.get_tmpfile_path(filename)
        tree = Tree(tmp)
        combined = Combined(tree.root)
        return combined, tree, tmp

    def test_getter(self):
        combined, tree, tmp = self._init_class('simple.mscx')
        self.assertEqual(combined.title, 'Title')
        self.assertEqual(combined.subtitle, None)
        self.assertEqual(combined.composer, 'Composer')
        self.assertEqual(combined.lyricist, None)

    def test_setter(self):
        combined, tree, tmp = self._init_class('simple.mscx')
        combined.title = 'T'
        combined.subtitle = 'S'
        combined.composer = 'C'
        combined.lyricist = 'L'
        tree.save()
        combined = Combined(tree.root)
        self.assertEqual(combined.metatag.workTitle, 'T')
        self.assertEqual(combined.metatag.movementTitle, 'S')
        self.assertEqual(combined.metatag.composer, 'C')
        self.assertEqual(combined.metatag.lyricist, 'L')

        self.assertEqual(combined.vbox.Title, 'T')
        self.assertEqual(combined.vbox.Subtitle, 'S')
        self.assertEqual(combined.vbox.Composer, 'C')
        self.assertEqual(combined.vbox.Lyricist, 'L')


class TestIntegration(unittest.TestCase):

    def test_distribute_field(self):
        tmp = helper.get_tmpfile_path('meta-distribute-field.mscx')
        mscxyz.execute(
            ['meta', '--distribute-field', 'vbox_title',
             '$combined_title - $combined_composer', tmp]
        )

        meta = Meta(tmp)
        iface = meta.interface

        self.assertEqual(iface.vbox_composer, 'Composer')
        self.assertEqual(iface.metatag_composer, 'Composer')
        self.assertEqual(iface.vbox_title, 'Title')
        self.assertEqual(iface.metatag_work_title, 'Title')

    def test_clean(self):
        tmp = helper.get_tmpfile_path('meta-all-values.mscx')
        mscxyz.execute(
            ['meta', '--clean', 'all', tmp]
        )

        meta = Meta(tmp)
        iface = meta.interface
        for field in iface.fields:
            self.assertEqual(getattr(iface, field), None, field)


if __name__ == '__main__':
    unittest.main()
