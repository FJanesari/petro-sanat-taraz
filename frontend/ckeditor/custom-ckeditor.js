import ClassicEditorBase from '@ckeditor/ckeditor5-build-classic';
import { ImageResize } from '@ckeditor/ckeditor5-image';

export default class ClassicEditor extends ClassicEditorBase {}

ClassicEditor.builtinPlugins = [
    ...ClassicEditorBase.builtinPlugins,
    ImageResize
];

ClassicEditor.defaultConfig = {
    toolbar: {
        items: [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'blockQuote',
            'imageUpload',
            '|',
            'undo',
            'redo'
        ]
    },
    image: {
        toolbar: [
            'imageTextAlternative',
            'imageStyle:inline',
            'imageStyle:block',
            'imageStyle:side',
            '|',
            'resizeImage',
            'resizeImage:50',
            'resizeImage:75',
            'resizeImage:original'
        ]
    },
    language: 'fa'
};
