import sublime
import sublime_plugin

import project
import settings
from util import check_settings, logger, packagemeta

log = logger(__name__)


class AndroidAuto(sublime_plugin.EventListener):
    """EventListener to handle enabled automatic events.

    Settings are configured on multiple hooks to keep up with class path changes.
    """
    @project.exists
    def on_load(self, view):
        settings.load(view)

    @project.exists
    def on_new(self, view):
        settings.load(view)

    @project.exists
    def on_post_save(self, view):
        settings.load(view)
        self.auto_build(view)

    @project.exists
    @packagemeta.requires("SublimeLinter")
    @check_settings("sublimeandroid_auto_build")
    def lint(self, view):
        import SublimeLinter
        SublimeLinter.reload_view_module(view)
        linter = SublimeLinter.select_linter(view)
        SublimeLinter.queue_linter(linter, view, preemptive=True, event='on_post_save')

    @check_settings("sublimeandroid_auto_build")
    def auto_build(self, view):
        # TODO
        # if not should_auto_build:
        #     return

        def callback():
            log.debug("calling SublimeLinter")
            self.lint(view)
        # ant_build(view, callback=callback, verbose=True)


class AndroidToggleAutoCommand(sublime_plugin.WindowCommand):
    def run(self):
        # TODO
        # global should_auto_build
        # should_auto_build = not should_auto_build
        # log.debug("Setting auto build value to %s", should_auto_build)
        settings.load(sublime.active_window().active_view())
        # self.window.active_view().settings().set("sublimeandroid_auto_build", auto)

    def is_visible(self):
        return project.exists()

    def is_enabled(self):
        return project.exists()
