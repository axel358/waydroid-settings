desktop_file = i18n.merge_file(
  input: 'cu.axel.waydroidsettings.desktop.in',
  output: 'cu.axel.waydroidsettings.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'cu.axel.waydroidsettings.appdata.xml.in',
  output: 'cu.axel.waydroidsettings.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('cu.axel.waydroidsettings.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

install_data('org.freedesktop.policykit.waydroid-helper.policy',
  install_dir: join_paths(get_option('datadir'), 'polkit-1/actions')
)

#install_subdir('scripts', install_dir: join_paths(get_option('datadir'), 'waydroid'))

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

subdir('icons')
