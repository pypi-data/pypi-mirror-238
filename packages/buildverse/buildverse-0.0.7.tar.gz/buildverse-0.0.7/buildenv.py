#!/usr/bin/python3
import hashlib
import os
import pathlib
from typing import Optional

import configenv
import quick
import sync


class BuildEnv:
    def __init__(self, reporoot: pathlib.Path | str):
        if not reporoot:
            raise Exception(f"Invalid reporoot: {reporoot}")
        self._reporoot: pathlib.Path = pathlib.Path(reporoot)
        self._configenv = configenv.ConfigEnv(self._reporoot.as_posix())

    def SyncBuildFiles(self):
        curfiledir = pathlib.Path(__file__).parent
        synclist = {
            "ci": None,
            "cmake": None,
            "include/CommonMacros.h": None,
            "include/TestUtils.h": None,
            "mingw_download.ps1": None,
            "externaltools.py": None,
            "clang-format": ".clang-format",
            "gitignore": ".gitignore",
            "gitattributes": ".gitattributes",
            "ref-pyproject.toml": "pyproject.toml",
        }

        tgtfiles: dict[str, pathlib.Path] = {}
        rootleveldirs: list[pathlib.Path] = list([d for d in self._reporoot.iterdir() if d.is_dir() and d.name != ".git"]) + [
            pathlib.Path()
        ]
        for d in rootleveldirs:
            scandir = self._reporoot / d
            if not scandir.exists():
                continue
            if scandir.name in synclist:
                for fpath in scandir.rglob("*"):
                    if not fpath.is_dir():
                        tgtfiles[fpath.relative_to(self._reporoot).as_posix()] = fpath
                        tgtfiles[fpath.name] = fpath
            else:
                for f in scandir.iterdir():
                    if f.is_file():
                        tgtfiles[f.as_posix()] = f
                        tgtfiles[f.name] = f
        for k, v in synclist.items():
            srcfs = [curfiledir / k]

            def expand_dirs(srcf: pathlib.Path):
                return list([fpath for fpath in srcf.rglob("*") if not fpath.is_dir()]) if srcf.is_dir() else [srcf]

            # flatten array of arrays
            srcfs = [file for srcf in srcfs for file in expand_dirs(srcf)]
            for srcf in srcfs:
                vname = pathlib.Path(v or srcf.as_posix()).name
                if vname in tgtfiles:
                    sync.Syncer.SyncFiles(srcf, tgtfiles[vname])

        file_quickdecl = self._reporoot / "quickload.config.ini"
        if file_quickdecl.exists():
            quickbuild = quick.Quick(self._reporoot)
            quickbuild.LoadConfig(file_quickdecl)
            quickbuild.VerifyLoaderCMake()

    @staticmethod
    def FindGitRoot(reporoot: pathlib.Path):
        curdir: pathlib.Path = reporoot
        while curdir.absolute() != curdir.parent.absolute():
            if (curdir / ".git").exists():
                return curdir
            curdir = curdir.parent
        return reporoot

    @staticmethod
    def GetProjectName(reporoot: pathlib.Path) -> str:
        projectname = reporoot.relative_to(BuildEnv.FindGitRoot(reporoot).parent).as_posix()
        projectname = projectname.replace("/", "_")
        return projectname

    def GetBinPath(self) -> pathlib.Path:
        return pathlib.Path(self._configenv.GetConfigPath("DEVEL_BINPATH", make=True))

    def GetTMPDownloadPath(self):
        return self._configenv.GetConfigPath("DEVEL_BINPATH", make=True)

    def ValidateDirectory(self, path: pathlib.Path):
        path.mkdir(exist_ok=True)
        return path

    def GetUniqueName(self, sdir: Optional[pathlib.Path] = None) -> str:
        srcdir: pathlib.Path = sdir or self._reporoot
        hashstr: str = hashlib.md5(srcdir.as_posix().lower().encode("utf-8")).hexdigest()[0:8]
        return f"{srcdir.name}_{hashstr}"

    def GetBaseBuildDir(self) -> pathlib.Path:
        return self._configenv.GetConfigPath("DEVEL_BUILDPATH", make=True) / self.GetUniqueName()

    def GetBuildScriptGenDir(self):
        return self.ValidateDirectory(self.GetBaseBuildDir() / "cmake")

    def GetBuildDir(self, mode: str, arch: str):
        return self.ValidateDirectory(self.GetBaseBuildDir() / f"{mode}_{arch}")

    def GetInstallDir(self, mode: str, arch: str):
        return self.ValidateDirectory(self.GetBaseBuildDir() / "install" / mode / arch)

    def GetPackagesDir(self):
        return self.ValidateDirectory(self.GetBaseBuildDir() / "packages")

    def GetFetchContentBaseDir(self):
        return self._configenv.GetConfigPath("DEVEL_BUILDPATH", make=True) / "externalsrcs"

    def GetVcpkgRoot(self):
        return self._configenv.GetConfigPath("VCPKG_ROOT", make=True)

    def GetNpmRoot(
        self,
    ):
        return self._configenv.GetConfigPath("NPM_BUILD_ROOT", make=True)
